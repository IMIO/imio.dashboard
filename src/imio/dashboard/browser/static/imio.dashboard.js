Faceted.Options.FADE_SPEED=0;
Faceted.Options.SHOW_SPINNER=false;

// Function that allows to generate a document aware of table listing documents in a faceted navigation.
function generatePodDocument(template_uid, output_format, tag) {
    theForm = $(tag).parents('form')[0];
    theForm.template_uid.value = template_uid;
    theForm.output_format.value = output_format;
    var hasCheckBoxes = 0;
    // if not checkboxes detected, do not manage uids, we are not on a table
    if (!$('input[name="select_item"]').length) {
        theForm.submit();
    }
    else {
        var uids = selectedCheckBoxes('select_item');
        if (!uids.length) {
            alert(no_selected_items);
        }
        else {
            // if we unselected some checkboxes, we pass uids
            // else, we pass nothing, it is as if we did selected everything
            if ($('input[name="select_item"]').length === uids.length) {
                uids = [];
            }
            // pass the facetedquery
            theForm.facetedQuery.value = JSON.stringify(Faceted.Query);
            theForm.uids.value = uids;
            theForm.submit();
        }
    }
}
