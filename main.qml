import QtQuick
import QtQuick.Controls.Basic

ApplicationWindow {
    visible: true
    width: 400
    height: 600
    x: screen.desktopAvailableWidth - width - 12
    y: screen.desktopAvailableHeight - height - 48
    title: "Astronomy Photo and Time"

    flags: Qt.FramelessWindowHint | Qt.Window

    property string currTime: "00:00:00" 
    property QtObject backend 
    
    Rectangle {
        anchors.fill: parent        
        
        Image {
            sourceSize.width: parent.width
            sourceSize.height: parent.height
            source: "./RAPOD.JPG"
            fillMode: Image.PreserveAspectFit        
        }        
        
        Rectangle {
            anchors.fill: parent
            color: "transparent"            
            
            Text {
                text: currTime
                font.pixelSize: 48
                color: "white"
            }        
        }     
          
    }

    Connections {
        target: backend
        function onUpdated(msg) {
            currTime = msg;
        }
    }
}