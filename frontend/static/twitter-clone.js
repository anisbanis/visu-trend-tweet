 function addTweet() {
      var html = $('<div>').append($('.tweet:last-child').clone()).remove().html();
      $(html).appendTo($.find('.tweets')).slideDown();
    }
    function addTenTweets() {
      for (var i = 0; i < 10; i++) {
       addTweet();
     }
    }
    $(document).ready(function(){
     
     $('.tweet-content').focus(function(){
      $('.new-tweet-footer').css('display', 'initial');
      $('.tweet-content').css('height', '100px');
     });
      $('.tweet-content').focusout(function(){
      $('.new-tweet-footer').css('display', 'none');
      $('.tweet-content').css('height', '20px');
     });


     addTenTweets()

     $(window).scroll(function () {
      if ($(window).scrollTop() >= $(document).height() - $(window).height() - 10) {

        setTimeout(function() {
            $('.loading').css('display', 'initial');
        }, 1000);

        setTimeout(function() {
            addTweet();
        }, 2000);

        setTimeout(function() {
            $('.loading').css('display', 'none');
        }, 2000);
    }
});

   })