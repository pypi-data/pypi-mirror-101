;(function (window, docuemnt, undefined) {

    window.WebSocketGateWay = function (groupName, messageHandler) {


        var protocol = window.location.protocol == 'https:' ? 'wss' : 'ws'
        this.ws = new WebSocket(protocol + '://' + window.location.host + '/ws');

        this.messionHandlersMap = {};
        var reqId = 0
        var eventData = {action: "subscribe", model: "asd", req_id: 1}
        var self = this

        this.subscribe = function (groupName, messageHandler) {
            this.messionHandlersMap[groupName] = this.messionHandlersMap[groupName] ? this.messionHandlersMap[groupName] : []
            this.messionHandlersMap[groupName].push(messageHandler)
            if (ws.readyState == WebSocket.OPEN) {
                this.sendEventData('subscribe', {model: groupName})
            } else {
                console.dir('Connection has lose.')
            }

        }

        this.sendEventData = function (action, data) {
            reqId += 1
            data.action = action
            data.req_id = reqId
            ws.send(JSON.stringify(data))
        }

        ws.onopen = function (event) {
            console.log("Connection open ...");
            if (groupName && messageHandler) {
                self.subscribe(groupName, messageHandler)
            }

        };
        ws.onmessage = function (event) {
            var eventData = JSON.parse(event.data);
            var groupName = eventData.model
            if (self.messionHandlersMap[groupName]) {
                for (var i in self.messionHandlersMap[groupName]) {
                    self.messionHandlersMap[groupName][i](eventData, event)
                }

            }
        };
        ws.onclose = function (event) {
            console.log("Connection closed.");
        };

        ws.onerror = function (event) {
            console.log("Connection onerror.");
        };

        return this
    }
})(window, document);