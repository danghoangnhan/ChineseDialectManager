    if request.POST:
        #Do something with post data here
    return render_to_response('form.html', locals(), context_instance = RequestContext(request))

def test_post(request):
    if request.POST:
        #Do something with post data here
    return render_to_response('form.html', locals(), context_instance = RequestContext(request))