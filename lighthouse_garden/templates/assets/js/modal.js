$('div[data-toggle="modal"]').on('click', function (event) {
  var button = $(this);
  var url = button.data('url');
  var target = button.data('target');
  var title = button.data('title');
  var modal = $(target);
  if (!url) {
    event.preventDefault();
  }
  modal.find('.modal-title').text(title);
  modal.find('.modal-body').html('<iframe src="' + url + '">');
  modal.find('.modal-body iframe').height(0.8 * $(document).height());
});