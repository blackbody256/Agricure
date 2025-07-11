from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model   # <-- Add this line
from diagnosis.models import Diagnosis
import plotly.express as px
import plotly.offline as opy
import pandas as pd

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
        line_graph = opy.plot(line_fig, auto_open=False, output_type='div')

        # Pie chart: Proportion of diseases detected
        pie_data = df['disease_name'].value_counts().reset_index()
        pie_data.columns = ['disease_name', 'count']
        pie_fig = px.pie(
            pie_data, names='disease_name', values='count',
            title='Diseases Detected (Proportion)', height=280
        )
        pie_fig.update_traces(textposition='inside', textinfo='percent+label')
        pie_fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
        pie_chart = opy.plot(pie_fig, auto_open=False, output_type='div')

        # Horizontal bar graph: Diseases detected
        bar_fig = px.bar(
            pie_data, x='count', y='disease_name', orientation='h',
            title='Diseases Detected (Count)', height=280
        )
        bar_fig.update_traces(marker_color='rgba(58, 71, 80, 0.8)', marker_line_width=2)
        bar_fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
        bar_graph = opy.plot(bar_fig, auto_open=False, output_type='div')

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



def admin_analytics(request):
    diagnoses = Diagnosis.objects.select_related('user').order_by('-timestamp')
    history = diagnoses.values('timestamp', 'disease_name', 'severity', 'affected_part', 'confidence', 'image', 'user__username')
    df = pd.DataFrame(list(history))
    if not df.empty:
        df['month'] = pd.to_datetime(df['timestamp']).dt.strftime('%b %Y')
        df['image_url'] = df['image'].apply(lambda img: settings.MEDIA_URL + str(img) if img else None)
        # Most recent detection
        most_recent = df.iloc[0]
        most_recent_detection = {
            'date': most_recent['timestamp'],
            'disease': most_recent['disease_name'],
            'image_url': most_recent['image_url'],
        }
        # Most common disease
        most_common_disease = df['disease_name'].mode()[0]
        # Line graph: Detections per month
        monthly_counts = df.groupby('month').size().reset_index(name='detections')
        line_fig = px.line(monthly_counts, x='month', y='detections', title='Detections Per Month', markers=True, height=280)
        line_graph = opy.plot(line_fig, auto_open=False, output_type='div')
        # Pie chart: Proportion of diseases detected
        pie_data = df['disease_name'].value_counts().reset_index()
        pie_data.columns = ['disease_name', 'count']
        pie_fig = px.pie(pie_data, names='disease_name', values='count', title='Diseases Detected (Proportion)', height=280)
        pie_chart = opy.plot(pie_fig, auto_open=False, output_type='div')
        # Horizontal bar graph: Diseases detected
        bar_fig = px.bar(pie_data, x='count', y='disease_name', orientation='h', title='Diseases Detected (Count)', height=280)
        bar_graph = opy.plot(bar_fig, auto_open=False, output_type='div')
        history_list = df.to_dict('records')
    else:
        most_recent_detection = {'date': '-', 'disease': '-', 'image_url': None}
        most_common_disease = '-'
        line_graph = pie_chart = bar_graph = None
        history_list = []

    # Total active users
    User = get_user_model()
    total_active_users = User.objects.filter(is_active=True).count()

    return render(request, 'analytics/admin_dashboard.html', {
        'line_graph': line_graph,
        'bar_graph': bar_graph,
        'pie_chart': pie_chart,
        'history': history_list,
        'most_recent_detection': most_recent_detection,
        'most_common_disease': most_common_disease,
        'total_active_users': total_active_users,
    })