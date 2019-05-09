import flask
import httplib2
from apiclient import discovery
from oauth2client import client

app = flask.Flask(__name__)
app.secret_key = 'jdfhkfjsdkfhKLKutdusyad'
app.debug = True

@app.route('/')
def index():
	flow = client.flow_from_clientsecrets('credentials.json',
			scope='https://www.googleapis.com/auth/drive.readonly',
			redirect_uri=flask.url_for('index', _external=True))
	flow.params['include_granted_scopes'] = 'true'
	if 'code' not in flask.request.args:
		auth_uri = flow.step1_get_authorize_url()
		return flask.redirect(auth_uri)
	else:
		auth_code = flask.request.args.get('code')
		credentials = flow.step2_exchange(auth_code)

		s = ""
    	http = credentials.authorize(httplib2.Http())
    	service = discovery.build('drive', 'v3', http=http)
    	results = service.files().list(
            pageSize=20,
            fields="nextPageToken, files(name)").execute()
    	items = results.get('files', [])
        for file in items:
            s += "%s<br>" % file['name']
        return s


if __name__ == '__main__':
	app.run()
