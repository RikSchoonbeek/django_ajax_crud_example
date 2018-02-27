$(function () {

  // Delete the selected book
  $.fn.deleteBook = function(){
    console.log('deleteBook function called');
    var button = $(this);
    console.log(button);

  }

  // Get the book list (table) and update the container to display the updated list
  $.fn.getBookList = function(){
        $.ajax({
        url: '/book_list/',
        type: 'get',
        dataType: 'json',
        success: function (data) {
          $("#book-table-container").html(data.book_list);

          $("#add-button").click(function () {
            $.ajax({
              url: '/add_book/',
              type: 'get',
              dataType: 'json',
              beforeSend: function () {
                $("#modal-book").modal("show");
              },
              success: function (data) {
                $("#modal-book .modal-content").html(data.html_form);
              }
            });
          });
        }
      });
    }

  // On loading of the page get the book list.
  $.fn.getBookList();

  $("#modal-book").on("submit", ".js-book-create-form", function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $.fn.getBookList();
        }
        else {
          $("#modal-book .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  });

  // Click event listener on #book-table-container with selector for .delete-book-btn
  // To delete selected book on click of delete button
  $("#book-table-container").on("click", ".delete-book-btn", function() {
    var button = $(this)
    $.ajax({
      url: button.attr("id"),
      type: 'get',
      dataType: 'json',
      success: function () {
        $.fn.getBookList();
      }
    });
  });


});