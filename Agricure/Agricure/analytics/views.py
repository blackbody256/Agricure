from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from diagnosis.models import Diagnosis
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import plot
import pandas as pd

User = get_user_model()

@login_required
def farmer_analytics(request):
    diagnoses = Diagnosis.objects.filter(user=request.user).order_by('-timestamp')
    history = diagnoses.values('timestamp', 'disease_name', 'severity', 'affected_part', 'confidence', 'image')
    if diagnoses.exists():
        df = pd.DataFrame(list(history))
        df['month'] = pd.to_datetime(df['timestamp']).dt.strftime('%b %Y')

        # Add image_url to each row
        def get_image_url(image):
            if image:
                return settings.MEDIA_URL + str(image)
            return None

        df['image_url'] = df['image'].apply(get_image_url)

        # Most recent detection
        most_recent = df.iloc[0]
        most_recent_detection = {
            'date': most_recent['timestamp'],
            'disease': most_recent['disease_name'],
            'image_url': most_recent['image_url'],
        }

        # Most common disease
        most_common_disease = df['disease_name'].mode()[0] if not df.empty else '-'

        # Line graph: Detections per month
        monthly_counts = df.groupby('month').size().reset_index(name='detections')
        line_fig = px.line(
            monthly_counts, x='month', y='detections',
            title='Detections Per Month', markers=True,
            height=280
        )
        line_fig.update_traces(line=dict(width=4), marker=dict(size=10))
        line_fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
        line_graph = plot(line_fig, output_type='div', include_plotlyjs=True)

        # Pie chart: Proportion of diseases detected
        pie_data = df['disease_name'].value_counts().reset_index()
        pie_data.columns = ['disease_name', 'count']
        pie_fig = px.pie(
            pie_data, names='disease_name', values='count',
            title='Diseases Detected (Proportion)', height=280
        )
        pie_fig.update_traces(textposition='inside', textinfo='percent+label')
        pie_fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
        pie_chart = plot(pie_fig, output_type='div', include_plotlyjs=True)

        # Horizontal bar graph: Diseases detected
        bar_fig = px.bar(
            pie_data, x='count', y='disease_name', orientation='h',
            title='Diseases Detected (Count)', height=280
        )
        bar_fig.update_traces(marker_color='rgba(58, 71, 80, 0.8)', marker_line_width=2)
        bar_fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
        bar_graph = plot(bar_fig, output_type='div', include_plotlyjs=True)

        history_list = df.to_dict('records')
    else:
        line_graph = None
        bar_graph = None
        pie_chart = None
        history_list = []
        most_recent_detection = {'date': '-', 'disease': '-', 'image_url': None}
        most_common_disease = '-'

    return render(request, 'analytics/farmer_dashboard.html', {
        'line_graph': line_graph,
        'bar_graph': bar_graph,
        'pie_chart': pie_chart,
        'history': history_list,
        'most_recent_detection': most_recent_detection,
        'most_common_disease': most_common_disease,
    })


def is_admin(user):
    return user.is_superuser or getattr(user, 'role', None) == 'ADMIN'

@login_required
@user_passes_test(is_admin)
def admin_analytics(request):
    # Check if user is admin
    if request.user.role != 'ADMIN':
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    
    # Get current date and month boundaries
    now = timezone.now()
    current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Basic statistics
    total_users = User.objects.filter(role='FARMER').count()
    total_diagnoses = Diagnosis.objects.count()
    unique_diseases = Diagnosis.objects.values('disease_name').distinct().count()
    monthly_diagnoses = Diagnosis.objects.filter(timestamp__gte=current_month_start).count()
    
    # User statistics
    new_users_this_month = User.objects.filter(
        date_joined__gte=current_month_start,
        role='FARMER'
    ).count()
    
    # Active users (users who made diagnoses in last 30 days)
    thirty_days_ago = now - timedelta(days=30)
    active_user_ids = Diagnosis.objects.filter(
        timestamp__gte=thirty_days_ago
    ).values_list('user__id', flat=True).distinct()
    
    active_users = User.objects.filter(
        id__in=active_user_ids,
        role='FARMER'
    ).count()
    
    # Average diagnoses per user
    avg_diagnoses_per_user = round(total_diagnoses / total_users if total_users > 0 else 0, 1)
    
    # Most active user
    user_diagnosis_counts = {}
    for diagnosis in Diagnosis.objects.select_related('user'):
        if diagnosis.user.role == 'FARMER':
            user_diagnosis_counts[diagnosis.user.username] = user_diagnosis_counts.get(diagnosis.user.username, 0) + 1
    
    most_active_user = max(user_diagnosis_counts, key=user_diagnosis_counts.get) if user_diagnosis_counts else "None"
    
    # Recent diagnoses (last 10)
    recent_diagnoses = Diagnosis.objects.select_related('user').order_by('-timestamp')[:10]
    
    # Top diseases
    top_diseases_data = Diagnosis.objects.values('disease_name').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Calculate percentages for top diseases
    top_diseases = []
    for disease in top_diseases_data:
        percentage = round((disease['count'] / total_diagnoses * 100) if total_diagnoses > 0 else 0, 1)
        top_diseases.append({
            'name': disease['disease_name'],
            'count': disease['count'],
            'percentage': percentage,
            'trend': 'stable'
        })
    
    # Create charts
    disease_pie_chart = None
    monthly_trends_chart = None
    user_activity_chart = None
    
    if total_diagnoses > 0:
        try:
            # Get ALL diagnoses for system-wide analysis
            all_diagnoses = Diagnosis.objects.all().values('timestamp', 'disease_name', 'user__username')
            df_all = pd.DataFrame(list(all_diagnoses))
            
            # Disease distribution pie chart
            disease_counts = df_all['disease_name'].value_counts().reset_index()
            disease_counts.columns = ['disease_name', 'count']
            
            if not disease_counts.empty:
                fig_pie = px.pie(
                    disease_counts, 
                    values='count', 
                    names='disease_name',
                    title='System-Wide Disease Distribution',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_pie.update_layout(
                    font=dict(size=12),
                    showlegend=True,
                    height=300,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                disease_pie_chart = plot(fig_pie, output_type='div', include_plotlyjs=True)
            
            # Monthly trends
            df_all['month'] = pd.to_datetime(df_all['timestamp']).dt.strftime('%Y-%m')
            monthly_counts = df_all.groupby('month').size().reset_index(name='count')
            
            if not monthly_counts.empty:
                fig_line = px.line(
                    monthly_counts, 
                    x='month', 
                    y='count',
                    title='Monthly Detection Trends (All Users)',
                    markers=True
                )
                fig_line.update_layout(
                    xaxis_title='Month',
                    yaxis_title='Number of Diagnoses',
                    height=300,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                monthly_trends_chart = plot(fig_line, output_type='div', include_plotlyjs=True)
            
            # User activity chart
            user_activity_counts = df_all['user__username'].value_counts().head(10).reset_index()
            user_activity_counts.columns = ['username', 'count']

            if not user_activity_counts.empty:
                fig_bar = px.bar(
                    user_activity_counts, 
                    x='username', 
                    y='count',
                    title='Top 10 Most Active Users',
                    color='count',
                    color_continuous_scale='Greens'
                )
                fig_bar.update_layout(
                    xaxis_title='Users',
                    yaxis_title='Number of Diagnoses',
                    height=400,
                    margin=dict(l=20, r=20, t=40, b=20),
                    bargap=0.6,
                    bargroupgap=0.1
                )
                fig_bar.update_traces(
                    width=0.4,
                    marker_line_width=1,
                    marker_line_color='rgba(0,0,0,0.2)'
                )
                user_activity_chart = plot(fig_bar, output_type='div', include_plotlyjs=True)
        
        except Exception as e:
            # Silent error handling - no debug output
            pass
    
    context = {
        'total_users': total_users,
        'total_diagnoses': total_diagnoses,
        'unique_diseases': unique_diseases,
        'monthly_diagnoses': monthly_diagnoses,
        'new_users_this_month': new_users_this_month,
        'active_users': active_users,
        'avg_diagnoses_per_user': avg_diagnoses_per_user,
        'most_active_user': most_active_user,
        'recent_diagnoses': recent_diagnoses,
        'top_diseases': top_diseases,
        'disease_pie_chart': disease_pie_chart,
        'monthly_trends_chart': monthly_trends_chart,
        'user_activity_chart': user_activity_chart,
    }
    
    return render(request, 'analytics/admin_dashboard.html', context)
