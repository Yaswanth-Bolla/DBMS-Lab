from jinja2 import Template

def generate_resume(data):
    template = Template("""
    <h1>{{ name }}</h1>
    <p>Email: {{ email }}</p>
    <p>Phone: {{ phone }}</p>
    <h2>Education</h2>
    <ul>
        {% for edu in education %}
        <li>{{ edu }}</li>
        {% endfor %}
    </ul>
    <h2>Experience</h2>
    <ul>
        {% for exp in experience %}
        <li>{{ exp }}</li>
        {% endfor %}
    </ul>
    <h2>Skills</h2>
    <ul>
        {% for skill in skills %}
        <li>{{ skill }}</li>
        {% endfor %}
    </ul>
    """)
    return template.render(data) 