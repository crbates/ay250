from django.conf.urls.defaults import patterns, url
#Definition of the two URL's for uploading to and querying thte database
urlpatterns = patterns('bibcollections.views',
    url(r'^query/$','query_database'),
    url(r'^upload/$','upload_file'),
    )
