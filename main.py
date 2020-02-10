from run import *
import web

web.config.debug = False
urls = (
    '/', 'Index',
    '/login', 'Login',
    '/logout', 'Logout'
)
global_render = web.template.render('templates')
render = web.template.render('templates', base='base', globals={'global_render':global_render})
app = web.application(urls, globals())
session = web.session.Session(
    app,
    web.session.DiskStore('sessions'),
    initializer={
        'logged_in':False,
        'username':'',
        'password':''
    }
)



class Index:
    def GET(self):
        input_data = web.input()
        run_data = {}
        if not session.logged_in:
            raise web.seeother('/login')
        run_main(input_data, run_data, session)
        return render.index(run_data)

    def POST(self):
        input_data = web.input()
        run_data = {}
        if not session.logged_in:
            raise web.seeother('/login')
        run_main(input_data, run_data, session)
        return render.index(run_data)



class Login:
    def GET(self):
        input_data = web.input()
        run_data = {}
        if session.logged_in:
            raise web.seeother('/')
        return render.login(run_data)

    def POST(self):
        input_data = web.input()
        run_data = {}
        run_login(input_data=input_data, run_data=run_data, session=session)
        if run_data['logged_in']:
            raise web.seeother('/')
        else:
            return render.login(run_data)



class Logout:
    def GET(self):
        input_data = web.input()
        run_data = {}
        run_logout(input_data, run_data, session)
        raise web.seeother('/')



if __name__ == "__main__":
    app.run()