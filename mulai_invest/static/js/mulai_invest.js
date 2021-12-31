// Referensi gambar grafik: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.upslide.net%2Fen%2Fways-to-make-beautiful-financial-charts-and-graphs-in-excel%2F&psig=AOvVaw1PF0lCk9rA9_6RkKMpRpnC&ust=1635618374547000&source=images&cd=vfe&ved=0CAgQjRxqFwoTCKiZhbSf8PMCFQAAAAAdAAAAABAD
// Referensi javascript grafik: https://bbbootstrap.com/snippets/chartjs-vertical-bar-chart-37115032

var month = new Array();
month[0] = "Januari";
month[1] = "Februari";
month[2] = "Maret";
month[3] = "April";
month[4] = "Mei";
month[5] = "Juni";
month[6] = "Juli";
month[7] = "Agustus";
month[8] = "September";
month[9] = "Oktober";
month[10] = "November";
month[11] = "Desember";

var sbx = new Array();
var bulan_angka = new Date().getMonth();
var usia_toko = parseInt(Math.random()*30);
var graph_start;

if(usia_toko>=6){
    graph_start=0;
} else{
    graph_start=6-usia_toko
}
for(let i=0; i<6; i++){
    if(bulan_angka-6+i<0){
        sbx[i]=month[12+bulan_angka-6+i];
        continue;
    }
    sbx[i]=month[bulan_angka-6+i];
}
var random_numb=Math.random()*70+5;
var net_sales = new Array();
for(let i=graph_start;i<6;i++){
    net_sales[i]=(random_numb + Math.random()*20).toFixed(2);
}

var gross_margin= new Array();
for(let i=graph_start;i<6;i++){
    gross_margin[i]=(net_sales[i]/(Math.random()*1+1.8)).toFixed(2);
}

var ebitda = new Array();
for(let i=graph_start; i<6; i++){
    ebitda[i]=(gross_margin[i]/(Math.random()*1+1.5)).toFixed(2);
}

var ctx1 = document.getElementById("bar_chart");
var myLineChart = new Chart(ctx1, {
    type: 'bar',
    data: {
        labels: sbx,
        datasets: [{
            data: net_sales,
            label: "Net Sales",
            borderColor: "#458af7",
            backgroundColor: '#458af7',
            fill: false
        }, {
            data: gross_margin,
            label: "Gross Margin",
            borderColor: "#8e5ea2",
            fill: true,
            backgroundColor: '#8e5ea2'
        }, {
            data: ebitda,
            label: "EBITDA",
            borderColor: "#3cba9f",
            fill: false,
            backgroundColor: '#3cba9f',
        }]
    },
    options: {
        scales: {
            xAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Bulan'
                }
            }],
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Nominal (dalam satuan juta)'
                },
                ticks: {
                    display: true,
                    suggestedMin: 0  
                }
            }]
        }  
    }
});


var gross_percentage = new Array();
for(let i=graph_start; i<6; i++){
    gross_percentage[i]=(gross_margin[i]*100/net_sales[i]).toFixed(2);
}

var ebitda_percentage = new Array();
for(let i=graph_start; i<6; i++){
    ebitda_percentage[i]=(ebitda[i]*100/net_sales[i]).toFixed(2);
}

var ctx2 = document.getElementById("line_chart");
var myLineChart = new Chart(ctx2, {
    type: 'line',
    data: {
        labels: sbx,
        datasets: [{
            data: gross_percentage,
            label: "% Gross margin over net sales",
            borderColor: "#8e5ea2",
            fill: false,
            backgroundColor: '#8e5ea2'
        }, {
            data: ebitda_percentage,
            label: "% EBITDA over net sales",
            borderColor: "#3cba9f",
            fill: false,
            backgroundColor: '#3cba9f'
        }]
    },
    options: {
        scales: {
            xAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Bulan'
                }
            }],
            yAxes: [{
                ticks: {
                    display: true,
                    suggestedMax: 100
                }
            }]
        }  
    }
});

$(window).on('resize', function(){
    resizeCanvas();
});

function resizeCanvas() {
    var canvas = $('#bar_chart');
    canvas.css("width", $(window).width()/2);
    canvas.css("height", $(window).height()/8);
    var canvas2 = $('#line_chart');
    canvas2.css("width", $(window).width()/2);
    canvas2.css("height", $(window).height()/8);
}


