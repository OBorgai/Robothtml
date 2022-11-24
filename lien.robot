*** Settings ***
Library    SeleniumLibrary
*** Variables ***
*** Test Cases ***
Tester llien de la page 
    Open Browser    https://www.selenium.dev/selenium/docs/api/java/index.html?overview-summary.html    gc
    Maximize Browser Window
    Sleep    3   
    Select Frame    name:packageListFrame
    Click link    org.openqa.selenium 
    Unselect Frame
    Sleep    3
    Select Frame    name:packageFrame
    Click Link    WebDriver
    Unselect Frame
    Sleep    3
    Select Frame    name:classFrame
    Click Link    Help
    Unselect Frame

    Sleep    3


    Close Browser

    