    $('document').ready(function(){

    // getting stats from html page
    stat=($("#stats").val()).replace(/\'/g,'"')
    //json object with stats
    s=JSON.parse(stat)

    if(s.accepted + s.wrong_answer + s.tle !==0){
    Highcharts.chart('container1', {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: 'Efficiency'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
        },
        series: [{
            name: 'Percentage',
            colorByPoint: true,
            data: [{
                name: 'TLE',
                y: s.tle
            }, {
                name: 'WA',
                y: s.wrong_answer
            }, {
                name: 'Accepted',
                y: s.accepted,
                sliced: true,
                selected: true
            }]
        }]
    });

    // calculation for the heat map
    attempt=($("#problem_attempt").val()).replace(/\'/g,'"').replace(/u"/g,'"')
    a=JSON.parse(attempt) 
    
    // date is a array of dicts storing month and week for  each submission 

    var date=[]

    for(var i=0;i<a.length;i++){
        var x=[]
        x=a[i].time.split("-"); 
        dict={}
        dict['month']=parseInt(x[1])
        dict['week']=Math.floor(parseInt(x[2].split(' ')[0])/7)
        date.push(dict)
        }

    //storing the number of attempts per week per month using a 2d list
    var heatMapList=[]
    for(var i=0;i<12;i++) 
        for(var j=0;j<5;j++)
        heatMapList.push([i,j,0])
    

    for(var i=0;i<date.length;i++)
    {
        var ind=(date[i]['month']-1)*5 +date[i]['week']
        heatMapList[ind][2]=1+heatMapList[ind][2]
    }

    console.log(heatMapList[16])

    Highcharts.chart('container2', {

        chart: {
            type: 'heatmap',
            marginTop: 40,
            marginBottom: 80,
            plotBorderWidth: 1
        },


        title: {
            text: 'Problems solved per month per week'
        },

        xAxis: {
            categories: ['Jan', 'Feb', 'Mar','April','May', 'Jun', 'Jul', 'Aug', 'Sept','Oct', 'Nov', 'Dec']
        },

        yAxis: {
            categories: ['Week1', 'Week2', 'Week3', 'Week4', 'Week5'],
            title: null
        },

        colorAxis: {
            min: 0,
            minColor: '#FFFFFF',
            maxColor: Highcharts.getOptions().colors[7]
        },

        legend: {
            align: 'right',
            layout: 'vertical',
            margin: 0,
            verticalAlign: 'top',
            y: 25,
            symbolHeight: 280
        },

        tooltip: {
            formatter: function () {
                return '<b>' +
                    this.point.value + '</b> problems in <br><b>' + this.series.yAxis.categories[this.point.y] + '</b>';
            }
        },

        series: [{
            name: 'Problems per week per month',
            borderWidth: 1,
            data: heatMapList, 
            dataLabels: {
                // enabled: true,
                color: '#000000'
            }
        }]

    });
}
});
