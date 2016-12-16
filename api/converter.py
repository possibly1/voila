import falcon
import requests
import json
import config

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Converter():
    url = '/'

    def prepareEmbed(self, formUid, formName):
        embedUrl = 'https://morphling1.typeform.com/to/' + formUid
        formName = formName
        formStyle =  'width:100%;height:500px;'
        embedCode = ('<!-- Change the width and height values to suit you best -->'
        '<div class="typeform-widget" data-url="__embed_url__" data-text="__form_name__" style="__style__"></div>'
        '<script>(function(){var qs,js,q,s,d=document,gi=d.getElementById,ce=d.createElement,gt=d.getElementsByTagName,id="typef_orm",b="https://s3-eu-west-1.amazonaws.com/share.typeform.com/";if(!gi.call(d,id)){js=ce.call(d,"script");js.id=id;js.src=b+"widget.js";q=gt.call(d,"script")[0];q.parentNode.insertBefore(js,q)}})()</script>'
        '<div style="font-family: Sans-Serif;font-size: 12px;color: #999;opacity: 0.5; padding-top: 5px;">Powered by<a href="https://www.typeform.com/examples/forms/?utm_campaign=__form_uid__&amp;utm_source=typeform.com-5872961-Basic&amp;utm_medium=typeform&amp;utm_content=typeform-embedded-onlineform&amp;utm_term=EN" style="color: #999" target="_blank">Typeform</a></div>')

        embedCode = embedCode.replace('__form_uid__', formUid)
        embedCode = embedCode.replace('__embed_url__', embedUrl)
        embedCode = embedCode.replace('__form_name__', formName)
        embedCode = embedCode.replace('__style__', formStyle)

        return embedCode

    def on_post(self, req, resp):
        if req.content_length:
            content = json.load(req.stream)

            headers = {'X-Typeform-Key': config.TYPEFORM_API_KEY}

            r = requests.post(config.TYPEFORM_API_CREATE_URL, headers = headers, data = json.dumps(content), verify=config.VERIFY_CREDENTIALS)
            #Link to typeform form
            # typeform_url = config.TYPEFORM_RENDER_BASE_URL + str(r.json()['id'])

            #Duplication link to land in the builder
            # typeform_duplicate_url = config.TYPEFORM_DUPLICATE_BASE_URL + str(r.json()['id']) + '?force_demo=true#landingPreview'

            dataFromApi = r.json()
            if 'id' in dataFromApi:
                id = str(dataFromApi['id'])

                embed = self.prepareEmbed(id, 'Form name should be here')

                resp.status = falcon.HTTP_200
                resp.content_type = 'application/json'
                resp.body = embed
            else:
                resp.status = falcon.HTTP_500
                resp.content_type = 'application/json'
                resp.body = json.dumps(dataFromApi)
        else:
            resp.status = falcon.HTTP_500
            resp.content_type = 'application/json'
            resp.body = '{Content has not been sent}'
