context.import_visits()

link = context.portal_url.getPortalObject().absolute_url()

state.setNextAction ('redirect_to:string:' + link)

return state