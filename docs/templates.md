# Template System Documentation

## Overview

The template system allows you to create, manage, and render dynamic dashboard templates. Templates support HTML, CSS, and JavaScript content with dynamic data binding capabilities.

## Template Types

- **Dashboard**: Full-page dashboards with multiple components
- **Report**: Structured data presentation templates
- **Widget**: Reusable dashboard components
- **Layout**: Base layouts for other templates

## Template Structure

### Basic Template
```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <style>
        /* CSS content */
        {{ css_content | safe }}
    </style>
</head>
<body>
    <!-- HTML content -->
    {{ html_content | safe }}
    
    <script>
        // JavaScript content
        {{ js_content | safe }}
    </script>
</body>
</html>
```

### Template Configuration

```json
{
  "type": "dashboard",
  "layout": {
    "grid": {
      "columns": 12,
      "rows": "auto"
    }
  },
  "theme": {
    "primary_color": "#007bff",
    "font_family": "Arial"
  },
  "components": [
    {
      "id": "chart1",
      "type": "line_chart",
      "position": {"x": 0, "y": 0, "w": 6, "h": 4}
    }
  ],
  "data_bindings": {
    "chart1": {
      "data_source": "sales_data",
      "mapping": {
        "x": "date",
        "y": "amount"
      }
    }
  }
}
```

## Template Inheritance

Templates can inherit from parent templates using the `parent_id` field.

### Parent Template Example
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
    {% block styles %}{% endblock %}
</head>
<body>
    <header>{% block header %}{% endblock %}</header>
    <main>{% block content %}{% endblock %}</main>
    <footer>{% block footer %}{% endblock %}</footer>
    {% block scripts %}{% endblock %}
</body>
</html>
```

### Child Template Example
```html
{% extends "parent_template" %}

{% block title %}Dashboard{% endblock %}

{% block content %}
<div class="dashboard">
    {{ components | safe }}
</div>
{% endblock %}
```

## Data Binding

### Static Data
```html
<div class="widget">
    <h2>{{ widget.title }}</h2>
    <p>{{ widget.description }}</p>
</div>
```

### Dynamic Data Source
```html
<div class="chart">
    <canvas id="myChart"></canvas>
</div>

<script>
const ctx = document.getElementById('myChart');
new Chart(ctx, {
    type: 'line',
    data: {{ chart_data | tojson }},
    options: {{ chart_options | tojson }}
});
</script>
```

## Template Lifecycle

1. **Draft**
   - Initial creation
   - Development and testing
   - Preview available

2. **Published**
   - Available for production use
   - Version controlled
   - Accessible via routes

3. **Archived**
   - Retired from active use
   - Preserved for reference
   - Can be restored

## Template Validation

The system validates:

1. HTML Structure
   - Valid HTML syntax
   - Required elements
   - Accessibility standards

2. CSS Content
   - Valid CSS syntax
   - Style conflicts
   - Browser compatibility

3. JavaScript Content
   - Valid JS syntax
   - Required dependencies
   - Security checks

4. Data Bindings
   - Valid data sources
   - Required fields
   - Type compatibility

## Best Practices

1. **Structure**
   - Use semantic HTML
   - Separate concerns (HTML/CSS/JS)
   - Follow component-based architecture

2. **Styling**
   - Use CSS variables for theming
   - Follow BEM naming convention
   - Implement responsive design

3. **JavaScript**
   - Use modern ES6+ features
   - Implement error handling
   - Follow event delegation pattern

4. **Data Binding**
   - Use clear naming conventions
   - Implement data validation
   - Handle loading states

## Example Templates

### Dashboard Template
```html
{% extends "base_dashboard" %}

{% block content %}
<div class="dashboard-grid">
    <div class="widget" data-source="sales">
        <h3>{{ widget.title }}</h3>
        <div class="chart">
            <canvas id="salesChart"></canvas>
        </div>
    </div>
    
    <div class="widget" data-source="inventory">
        <h3>{{ widget.title }}</h3>
        <table class="data-table">
            {% for item in items %}
            <tr>
                <td>{{ item.name }}</td>
                <td>{{ item.quantity }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</div>

{% block scripts %}
<script>
document.addEventListener('DOMContentLoaded', () => {
    initializeDashboard({
        refreshInterval: 60000,
        dataSources: ['sales', 'inventory']
    });
});
</script>
{% endblock %}
```

### Widget Template
```html
<div class="widget-container">
    <div class="widget-header">
        <h3>{{ title }}</h3>
        <div class="widget-controls">
            <button onclick="refreshWidget()">
                <i class="fas fa-sync"></i>
            </button>
        </div>
    </div>
    
    <div class="widget-content">
        {% if loading %}
        <div class="loading-spinner"></div>
        {% else %}
        {{ content | safe }}
        {% endif %}
    </div>
    
    <div class="widget-footer">
        <span class="last-updated">
            Updated: {{ last_updated | datetime }}
        </span>
    </div>
</div>
``` 