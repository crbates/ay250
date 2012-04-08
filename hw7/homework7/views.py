#home page view rendering function
from django.shortcuts import render_to_response
from bibcollections.models import Bibcollection
from django.core.management import call_command

def home(request):
    '''
    This function checks if the sqlite3 database exists. If it doesn't it creates
    the database. If it does exist it lets the user know if it has been populated.
    If it has been populated the names of the collections are displayed in a 
    bulleted list.
    '''
    db = None
    coll = None
    #try to determine number of collections if it raises an exception create a 
    #database 
    try:
        dblen = len(Bibcollection.objects.all())
    except:
        db = "No database exists one has been created"
        call_command('syncdb',interactive=False)
    else:
        #determine if the database has been populated
        if dblen > 0:
            db = "Database and collections present"
            coll = Bibcollection.objects.all()
        else:
            db = "Database present but no collections exist"
    return render_to_response('index.html',{'db':db,'coll':coll})
    
