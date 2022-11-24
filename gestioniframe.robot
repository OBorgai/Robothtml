*** Settings ***
Library    SeleniumLibrary
*** Variables ***
*** Test Cases ***
Test gerer une alerte
    Open Browser    http://omayo.blogspot.com/    gc
    Maximize Browser Window
    Sleep    3
   
    Close Browser   