
/*
qouates and rates
*/
var listRev = [
    { quote: "Choosing AlSalam was a good choice for me they gave us the best offer and the company have good references in lebanon so we could make our decision. ", author: "Ali N.Allow" },
    { quote: "Good customer service less than 1 hour they reply, my deal will be always with them.", author: "Jonas Schmidt" },
    { quote: "About price it seems good and cheap for me less price we a good quality keep going.", author: "Nawal Chame" },
    { quote: "I didnt get more treatment as i get from this company more than that fast shipping .", author: "Adam Kowalski" },
    { quote: "I ordered 5000 sheeps and 200 cattles all of them are in good shape, i didnt athought that they will come to my farm in less time that i think .", author: "Khaled M.Khaled" },
    { quote: "5 business and more with AlSalam company, they were so helpful and professional that we could choose good quality livestock That has been a good reference for us..", author: "Nouh Mussaa" },
    { quote: "In adha holiday i was searching for a deal in  a low price and good quality i just found this company! thank you.", author: "Mohammad Ahmad" },
    { quote: "25 years in business with good servers.", author: "Ismael Suliman" },
    { quote: "Nothing important in livestock more than good meat and milk best for more AlSalama", author: "Mark Nowicki" },
    
];

var currentQuote = 0;
var progress = setInterval(timerProgress, 10);
var progressWidth = 0;

// var timeDisplayed = 10000;
// var timer = setInterval(changeQuote, timeDisplayed);

function timerProgress() {
    $(".quote-progress").width(progressWidth + "%");
    if (progressWidth < 100) {
        progressWidth += 0.1;
    } else {
        changeQuote();
        progressWidth = 0;
    }
}

function setQuote() {
    $(".quote").html('"' + listRev[currentQuote].quote + '"');
    $(".author-name").html(listRev[currentQuote].author);
    rew();
}

function getRandomQuote() {
    currentQuote = Math.round(Math.random() * (listRev.length));
    setQuote();
}

function changeQuote() {
    // $("blockquote").fadeToggle( "slow", "linear" );
    if (currentQuote < listRev.length - 1) {
        currentQuote++;
    } else {
        currentQuote = 0;
    }
    setQuote();
}

$(".previous").click(function () {
    if (currentQuote > 0) {
        currentQuote--;
    } else {
        currentQuote = listRev.length - 1;
    }
    setQuote();
    progressWidth = 0;
});

$(".next").click(function () {
    changeQuote();
    progressWidth = 0;
});

$(".random").click(function () {
    getRandomQuote();
    progressWidth = 0;
});



function rew() {
    $('#quote-tweet').attr( encodeURIComponent('"' + listRev[currentQuote].quote + '" ' + listRev[currentQuote].author));
}

setQuote();