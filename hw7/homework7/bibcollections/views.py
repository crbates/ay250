#This file contains the functions for rendering the query and upload pages
from forms import DocumentForm
from models import Bibcollection, Article
from pybtex.database.input import bibtex
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.management import call_command
import string

def parseitem(item,field):
    '''
    This function is used to safely parse items from pybtex.
    '''
    # read the key value and remove any { } charachters
    try:    
        title = item.fields[field]
        title = string.replace(title,"{",'')
        title = string.replace(title,"}",'')
    except KeyError:
        
        title = ''
    return title


def upload_file(request):
    #render the upload file page and handle file uploads
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            #read file in and name of collection
            data = request.FILES['docfile'].read()
            newdoc = Bibcollection(bibfile = request.FILES['docfile'])
            newdoc.name = request.POST['name']
            newdoc.save()
            newdoc = Bibcollection.objects.get(pk= newdoc.id)
            parser  = bibtex.Parser()
            #write uploaded .bib to a temporary file
            f = open('temp.bib','w')
            f.write(data)
            f.close()
            result = parser.parse_file('temp.bib')
            #add entries to the collection
            for entry in result.entries.keys():
                item = result.entries[entry]
                title = parseitem(item,'title')     
                author = parseitem(item,'author')
                volume = parseitem(item,'volume')
                pages = parseitem(item,'pages')
                year = parseitem(item,'year')    
                journal = parseitem(item,'journal')    
                tag = entry
                itemtype = result.entries[entry].type
                newdoc.article_set.create(itemtype = itemtype, title = title, 
                author = author, volume = volume, pages = pages, year = year,
                tag = tag, journal = journal,collection_name=newdoc.name)
                
    else:
        # instantiate an empty form
        form = DocumentForm() 
    #build a database if one doesnt exist    
    try:
        dblen = len(Bibcollection.objects.all())
    except:
        call_command('syncdb',interactive=False)  
    #render the page      
    return render_to_response('upload.html', {'form':form},
    context_instance=RequestContext(request))

def query_database(request):
    '''
    This function renders the database query page. If the database doesn't exist
    or is empty the user is informed. 
    '''
    db = None
    #Check if the database exists
    try:
        dblen = len(Bibcollection.objects.all())
    except:
        db = "No database exists so one has been created. Please add a collection \
              before querying the database"
        call_command('syncdb',interactive=False)
    else:
        #check if the database is empty
        if dblen > 0:
            pass
        else:
            db = "Please add a collection before querying the database"
    error = None
    #Run the submitted query
    if request.method == 'POST':
        sql_cmd = 'select * from bibcollections_article where ' + request.POST['cmd']
        res = Article.objects.raw(sql_cmd)
        try:
            temp = res[0]
        except:
            res = None
            error = "Bad SQL statement"
        
    else:
        res =  None
    #Render the page with results
    return render_to_response('query.html',{'items':res,'error':error,'db':db},context_instance=RequestContext(request))
    
    
