$(document).ready(function () {
  Faceted.Options.FADE_SPEED=0;
  Faceted.Options.SHOW_SPINNER=false;
});


/* initialize overlays of portlet used for dahboards displaying contacts */
$(document).ready(function(){
  $('.add_contact_overlay').prepOverlay({
      subtype: 'ajax',
      closeselector: '[name="form.buttons.cancel"]'
  });
});
