*** Settings ***
Documentation  imio.dashboard on a faceted dashboard: javascript options, combined indexes in the faceted
...            configuration and in the faceted query. Version-independent: Plone selectors are in ui_plone*.robot.
Resource  dashboard.robot
Test Setup  Open a manager browser
Test Teardown  Close all browsers


*** Test Cases ***
The dashboard javascript disables the spinner and the fading
    [Documentation]  eea.facetednavigation defaults: SHOW_SPINNER true, FADE_SPEED 'fast'
    Open the dashboard
    The faceted option is  SHOW_SPINNER  ${False}
    The faceted option is  FADE_SPEED  ${0}

The faceted configuration offers the combined indexes
    Open the add widget form  folder  checkbox
    ${label}=  The index label  review_state
    The index select offers  combined__review_state  (Combined) ${label}
    ${label}=  The index label  contained_types_and_states
    The index select offers  combined__contained_types_and_states  (Combined) ${label}

A combined criterion filters the dashboard results
    [Documentation]  Data of test_combined_index: Folder 1 contains a private and a published page, Folder 2 is
    ...              empty, Folder 3 contains a private folder and a private page. c10 filters
    ...              contained_types_and_states on the portal type, c11 combines the review state with it.
    Open the dashboard
    The results list  Folder 1  Folder 2  Folder 3  Private folder
    Show the advanced filters
    # only the combined criterion: used as the real index
    Click the filter value  c11  private
    The results list  Folder 1  Folder 3
    The results do not list  Folder 2  Private folder
    # portal type Document combined with the review state published: Document__published
    Click the filter value  c11  private
    Click the filter value  c11  published
    Click the filter value  c10  Document
    The results list  Folder 1
    The results do not list  Folder 2  Folder 3  Private folder
