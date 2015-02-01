function make_stacked_area_chart(chart_data, xAxisCategories) {
    $('#area-chart').highcharts({
        chart: {
            type: 'area'
        },
        title: {
            text: "T&R's Savings"
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            categories: xAxisCategories,
            tickmarkPlacement: 'on',
            title: {
                enabled: false
            }
        },
        yAxis: {
            title: {
                text: 'Thousands (£)'
            },
            labels: {
                formatter: function () {
                    return this.value / 1000;
                }
            }
        },
        tooltip: {
            shared: true,
            valuePrefix: "£",
            valueSuffix: ''
        },
        plotOptions: {
            area: {
                stacking: 'normal',
                lineColor: '#666666',
                lineWidth: 1,
                marker: {
                    lineWidth: 1,
                    lineColor: '#666666'
                }
            }
        },
        series: chart_data
    });
}

function make_pie(data) {
    $('#pie-chart').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        title: {
            text: 'All time spend by category'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>£{point.y:.1f}</b>'
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
            type: 'pie',
            name: 'Browser share',
            data: data
        }]
    });
}

$(function () {
    $.ajax({
        type: "GET",
        url: "/api/account_totals/?accounts=Fidelity,Hargreaves%20Lansdown,Funding%20Circle,Deposit,Rhi%20Save,Savings%20(travel)",
        contentType: "application/json"
    }).done(function(data){
        var chart_data = [];
        var xAxisCategories = [];
        $.each(data, function(i, account) {
            var account_data = {"name": account.name, "data": []}
            $.each(account.months, function (j, month) {
                xAxisCategories.push(month.label);
                account_data.data.push(month.net_total)
            });
            chart_data.push(account_data)
        })
        make_stacked_area_chart(chart_data, xAxisCategories);
    }).fail(function(){
        console.log("FAIL!")
    })
    $.ajax({
        type: "GET",
        url: "/api/categories_by_month/",
        contentType: "application/json"
    }).done(function(data){
        console.log(data);
        make_pie(data)
    }).fail(function(){
        console.log("FAIL!")
    })
});