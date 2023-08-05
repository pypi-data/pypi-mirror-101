"""
Unit Testing For (API {{ name }})
"""

from flask import url_for
from flask.testing import FlaskClient

{% for spec in specs %}
def test_{{spec["name"]}}(client: FlaskClient):
    paths = {{ spec["paths"] }}
    url = url_for("{{ spec["endpoint"] }}", **paths)
    query = {{ spec["data"].pop("query", {}) }}
    {% set files = spec["data"].pop("files", {}) -%}
    files = {{ files }}
    {% for data_type in spec["data"].keys() -%}
    data = {{ spec["data"][data_type] }}
    {% if data_type == 'json' -%}
    resp = client.{{ spec["method"] | lower}}(url, json=data, query_string=query)
    {%- else %}
    {%- if files -%}
    data.update(files)
    {% endif -%}
    headers = {
        "Content-Type": {{ '"multipart/form-data"' if files else '"application/x-www-form-urlencoded"' }}
    }
    resp = client.{{ spec["method"] | lower}}(url, data=data, query_string=query, headers=headers)
    {%- endif -%}
    {% else -%}
    resp = client.{{ spec["method"] | lower}}(url, query_string=query)
    {%- endfor %}
    assert True
{% endfor %}
