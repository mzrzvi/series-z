$(function() {
  $('table.with-pager').each(function() {
      var $table = $(this);
      var $nextPage = $('.pager .next');
      var $previousPage = $('.pager .previous');
  
      var currentPage = 0;
      var numPerPage  = 3;
  
      var numRows  = 0;
      var numPages = 0;
  
      $table.bind('repaginate', function() {
          numRows  = $table.find('tbody tr').length;
          numPages = Math.ceil(numRows / numPerPage);
  
          $table.find('tbody tr').hide().slice(currentPage * numPerPage, (currentPage + 1) * numPerPage).show();
  
          if (currentPage == 0) {
              $previousPage.addClass('disabled');
          } else {
              $previousPage.removeClass('disabled');
          }
  
          if (currentPage == numPages-1) {
              $nextPage.addClass('disabled');
          } else {
              $nextPage.removeClass('disabled');
          }
      });
  
      $table.trigger('repaginate');
  
      $previousPage.bind('click', function(event) {
          if (currentPage != 0) {
              currentPage--;
              $table.trigger('repaginate');
          }
      });
  
      $nextPage.bind('click', function(event) {
          if (currentPage != numPages-1) {
              currentPage++;
              $table.trigger('repaginate');
          }
      });
  });
});
