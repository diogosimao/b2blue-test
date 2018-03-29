jQuery.noConflict()(function ($) {
    $(document).ready(function(){

        var mySlider = $("#id_price_slider").slider({tooltip: 'always'});

        $("#id_price_slider").on("change paste keyup", function() {
            var value = mySlider.slider('getValue');
            $("#id_price__gte").val(value[0]);
            $("#id_price__lte").val(value[1]);
        });
    });
});