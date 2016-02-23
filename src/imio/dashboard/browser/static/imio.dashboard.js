Faceted.Options.FADE_SPEED=0;
Faceted.Options.SHOW_SPINNER=false;

// Function that allows to generate a document aware of table listing documents in a faceted navigation.
function generatePodDocument(template_uid, output_format, tag) {
    theForm = $(tag).parents('form')[0];
    theForm.template_uid.value = template_uid;
    theForm.output_format.value = output_format;
    // manage the facetedquery
    theForm.facetedQuery.value = JSON.stringify(Faceted.Query);
    var hasCheckBoxes = 0;
    // if not checkboxes detected, do not manage uids, we are not on a table
    if ($('input[name="select_item"]').length) {
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
            theForm.uids.value = uids;
        }
    }
    theForm.submit();
}

$(document).ready(function () {
  var url = $('base').attr('href') + '/@@ajax_render_dashboard_portlet';
  $(Faceted.Events).bind(Faceted.Events.AJAX_QUERY_SUCCESS, function() {
      $.get(url, function (response) {
          $('.faceted-tagscloud-collection-widget').html(response);
      })
  });
})
