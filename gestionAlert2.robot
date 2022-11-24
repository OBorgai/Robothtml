*** Settings ***
Library    SeleniumLibrary
*** Variables ***
*** Test Cases ***
Test gerer une alerte
    Open Browser    http://omayo.blogspot.com/    gc
    Maximize Browser Window
    Sleep    3
    Click Button    xpath=//*[@id="alert1"]
    Sleep    3
    #Alert Should Be Present    Hello
    ${messageAlert}    Handle Alert 
    Log To Console    ${messageAlert} 
    Should Be Equal    ${messageAlert}    Hello  
    ${urlsite}    Get Location
    Log To Console    ${urlsite}
    Should Be Equal    ${urlsite}     http://omayo.blogspot.com/
    Close Browser    