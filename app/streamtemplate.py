from app import app

def stream_template(template_name, **context):                                                                                                                                                 
    app.update_template_context(context)                                                                                                                                                       
    t = app.jinja_env.get_template(template_name)                                                                                                                                              
    rv = t.stream(context)                                                                                                                                                                     
    rv.disable_buffering()                                                                                                                                                                     
    return rv