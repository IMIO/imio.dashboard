*** Settings ***
Documentation  imio.dashboard keywords, built on the ui_plone${PLONE_MAJOR}.robot keywords.
...            Robot Framework 3.1 syntax (FOR ... END; shared with the Plone 4.3 environment, RF 3.2.2).
...            Fixture (testing.COMBINED_INDEX_FIXTURE): dashboard "Folder" (/folder), default collection "Folders" (the
...            Folders of the site), checkboxes criteria c10 (portal type) and c11 (review state, combined) in the
...            advanced section, on the index contained_types_and_states. Paths are relative to the site.
...            Selectors: eea.facetednavigation, collective.eeafaceted.* and this package.
Resource  ui_plone${PLONE_MAJOR}.robot


*** Variables ***
${RESULTS}  css=#faceted-results
${ADD_WIDGET_FORM}  css=#faceted-edit-addwidget


*** Keywords ***
Open a manager browser
    Open test browser
    Set window size  1280  2000
    Enable autologin as  Manager

Open the dashboard
    [Arguments]  ${path}=folder
    Go to  ${PLONE_URL}/${path}
    The faceted results are loaded

The faceted results are loaded
    Wait until page contains element  ${RESULTS}
    Wait until element is not visible  css=.faceted-lock-overlay

The faceted option is
    [Documentation]  Value of the eea.facetednavigation javascript option Faceted.Options.${name}
    [Arguments]  ${name}  ${expected}
    ${value}=  Execute javascript  return Faceted.Options.${name};
    Should be equal  ${value}  ${expected}

Open the add widget form
    [Documentation]  eea faceted configuration (configure_faceted.html): "+" button of the first position,
    ...              widget type ${widget_type}
    [Arguments]  ${path}  ${widget_type}
    Go to  ${PLONE_URL}/${path}/configure_faceted.html
    Wait until page contains element  css=.faceted-add-button span
    Click element  css=.faceted-add-button span
    Wait until element is visible  ${ADD_WIDGET_FORM}
    Select from list by value  ${ADD_WIDGET_FORM} select#wtype  ${widget_type}

The index select offers
    [Documentation]  Option ${index} of the index select of the add widget form, with its label
    [Arguments]  ${index}  ${label}
    ${text}=  The index label  ${index}
    Should be equal  ${text}  ${label}

The index label
    [Documentation]  Label of the option ${index} of the index select of the add widget form
    [Arguments]  ${index}
    ${option}=  Set variable  ${ADD_WIDGET_FORM} .field-c0-faceted-c0-index select option[value="${index}"]
    Wait until page contains element  ${option}
    # retried: the add widget form re-renders its fields after the widget type is selected (stale element)
    ${text}=  Wait until keyword succeeds  10s  0.5s  Get text  ${option}
    [Return]  ${text}

Show the advanced filters
    [Documentation]  eea "More filters" link (widgets of the section "advanced")
    Click link  css=.faceted-sections-buttons-more
    Wait until element is visible  css=.faceted-advanced-widgets

Click the filter value
    [Documentation]  Checkbox ${value} (vocabulary token) of the checkboxes widget ${widget}
    [Arguments]  ${widget}  ${value}
    # its label, retried: eea 16 checkboxes scroll in a 100px high box and the advanced section is
    # still sliding down, geckodriver can't scroll the checkbox into view (ElementNotInteractable)
    ${id}=  Get element attribute  css=#${widget}_widget input[value="${value}"]  id
    Wait until keyword succeeds  10s  0.5s  Click element  css=#${widget}_widget label[for="${id}"]
    The faceted results are loaded

The results list
    [Arguments]  @{titles}
    FOR  ${title}  IN  @{titles}
        Wait until element contains  ${RESULTS}  ${title}
    END

The results do not list
    [Arguments]  @{titles}
    FOR  ${title}  IN  @{titles}
        Wait until keyword succeeds  10s  0.5s  Element should not contain  ${RESULTS}  ${title}
    END
