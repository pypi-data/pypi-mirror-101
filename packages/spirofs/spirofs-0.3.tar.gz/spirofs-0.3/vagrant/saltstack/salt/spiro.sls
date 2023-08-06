{% if grains['os_family'] == 'Debian' %}

{% if grains['pythonversion'][0] == 2 %}
python-pip: pkg.installed
{% else %}
python3-pip: pkg.installed
{% endif %}

ssl-cert: pkg.installed

{% elif grains['os_family'] == 'RedHat' %}

{% if grains['pythonversion'][0] == 2 %}
python27-pip: pkg.installed
{% else %}
python36-pip: pkg.installed
{% endif %}

{% endif %}
