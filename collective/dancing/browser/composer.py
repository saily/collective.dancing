import zope.publisher
from zope import schema
import zope.event
import z3c.form

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import Products.CMFPlone.utils
from collective.singing.interfaces import IComposer
from plone.z3cform.crud import crud

from plone.z3cform import z2
from zope import component
from zope.app.pagetemplate import viewpagetemplatefile
import collective.singing.interfaces
from collective.dancing import MessageFactory as _
from collective.dancing import collector
from collective.dancing.browser import controlpanel

from collective.dancing.interfaces import IHTMLComposer
from collective.dancing.browser.channel import EditComposersForm

class EditComposerForm(z3c.form.subform.EditSubForm):
    """Composer edit form.
    This allows editing of composers settings.
    """
    component.adapts(collective.singing.interfaces.IComposer,
                     zope.publisher.interfaces.http.IHTTPRequest,
                     z3c.form.form.EditForm)

    template = viewpagetemplatefile.ViewPageTemplateFile('subform.pt')
    description = _(u"Edit the properties of the composer.")
    format = u""

    @property
    def fields(self):
        return z3c.form.field.Fields(IComposer).omit('name', 'schema', 'title')

    @property
    def heading(self):
        return _(u"Composer for format : ${format}", mapping={'format':self.format})

    @property
    def prefix(self):
        return 'composers.%s.' % self.format

    @z3c.form.button.handler(EditComposersForm.buttons['save'])
    def handleSave(self, action):
        data, errors = self.widgets.extract()
        if errors:
            self.status = self.formErrorsMessage
            return
        content = self.getContent()
        changed = z3c.form.form.applyChanges(self, content, data)
        if changed:
            zope.event.notify(
                zope.lifecycleevent.ObjectModifiedEvent(content))
            self.status = self.successMessage
        else:
            self.status = self.noChangesMessage


class EditHTMLComposerForm(EditComposerForm):
    """HTMLComposer edit form.
    """
    component.adapts(collective.dancing.interfaces.IHTMLComposer,
                     zope.publisher.interfaces.http.IHTTPRequest,
                     z3c.form.form.EditForm)

    @property
    def fields(self):
        return z3c.form.field.Fields(IHTMLComposer).omit('name', 'schema', 'title')    
