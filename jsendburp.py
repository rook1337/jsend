import re
from burp import IBurpExtender, ITab, IHttpListener
from javax.swing import JPanel, JButton, JTextArea, JScrollPane
from java.awt import BorderLayout

class BurpExtender(IBurpExtender, ITab, IHttpListener):
    def __init__(self):
        self.requests = []

    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()

        # Set the extension name
        self._callbacks.setExtensionName("JSend")

        # Create GUI
        self.createGUI()

        # Register the extension as an HTTP listener
        callbacks.registerHttpListener(self)

        # Add the extension as a custom tab
        callbacks.addSuiteTab(self)

    def createGUI(self):
        self.panel = JPanel()
        self.panel.layout = BorderLayout()

        self.buttonRetrieve = JButton("Retrieve Requests", actionPerformed=self.retrieveRequests)
        self.panel.add(self.buttonRetrieve, BorderLayout.NORTH)

        self.buttonClear = JButton("Clear Requests", actionPerformed=self.clearRequests)
        self.panel.add(self.buttonClear, BorderLayout.SOUTH)

        self.textArea = JTextArea()
        scrollPane = JScrollPane(self.textArea)
        self.panel.add(scrollPane, BorderLayout.CENTER)

        self._callbacks.customizeUiComponent(self.panel)

    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        if not messageIsRequest:
            response = messageInfo.getResponse()
            url = messageInfo.getUrl().toString()
            self.requests.append((url, response))

    def retrieveRequests(self, event):
        regex = r"(?:\"|\')(((?:[a-zA-Z]{1,10}://|//)[^\"\'/]{1,}\.[a-zA-Z]{2,}[^\"\']{0,})|((?:/|\.\./|\./)[^\"\'><,;| *()(%%$^/\\\[\]][^\"\'><,;|()]{1,})|([a-zA-Z0-9_\-/]{1,}/[a-zA-Z0-9_\-/]{1,}\.(?:[a-zA-Z]{1,4}|action)(?:[\?|#][^\"|\']{0,}|))|([a-zA-Z0-9_\-/]{1,}/[a-zA-Z0-9_\-/]{3,}(?:[\?|#][^\"|\']{0,}|))|([a-zA-Z0-9_\-]{1,}\.(?:php|asp|aspx|jsp|json|action|html|js|txt|xml)(?:[\?|#][^\"|\']{0,}|)))(?:\"|\')"
        for request in self.requests:
            url = request[0]
            response = self._helpers.bytesToString(request[1])
            endpoints = re.findall(regex, response)
            self.textArea.append(url + "\n")
            for endpoint in endpoints:
                self.textArea.append(endpoint[0] + "\n")
            self.textArea.append("\n\n\n")

    def clearRequests(self, event):
        self.requests = []
        self.textArea.setText("")

    def getTabCaption(self):
        return "JSend"

    def getUiComponent(self):
        return self.panel

if __name__ in ["__main__", "burp"]:
    BurpExtender()

