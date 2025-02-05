// إعداد الرسم البياني لمبيعات المنتجات
document.addEventListener("DOMContentLoaded", function () {
    var salesMonths = JSON.parse(document.getElementById("salesChart").getAttribute('data-sales-months'));
    var salesData = JSON.parse(document.getElementById("salesChart").getAttribute('data-sales-data'));

    var optionsSales = {
        chart: {
            type: 'line',
            height: 350,
        },
        series: [{
            name: 'المبيعات',
            data: salesData
        }],
        xaxis: {
            categories: salesMonths,
            title: {
                text: 'الأشهر'
            }
        },
        yaxis: {
            title: {
                text: 'قيمة المبيعات'
            }
        }
    };

    var salesChart = new ApexCharts(document.querySelector("#salesChart"), optionsSales);
    salesChart.render();
});

//=========================الشكل الخاص بالبائعين و المستخدمين=============================


document.addEventListener("DOMContentLoaded", function () {
    // الحصول على البيانات من عناصر HTML
    const userCounts = JSON.parse(document.getElementById("userChart").getAttribute("data-user-counts"));
    const sellerCounts = JSON.parse(document.getElementById("userChart").getAttribute("data-seller-counts"));
    const months = JSON.parse(document.getElementById("userChart").getAttribute("data-months"));

    // إعدادات الرسم البياني
    var optionsUser = {
        chart: {
            type: 'bar',
            height: 350,
        },
        series: [
            {
                name: 'عدد المستخدمين',
                data: userCounts
            },
            {
                name: 'عدد البائعين',
                data: sellerCounts
            }
        ],
        colors: ['#1E90FF', '#FF6347'], // اللون الأزرق للمستخدمين والأحمر للبائعين
        xaxis: {
            categories: months,
            title: {
                text: 'الأشهر'
            }
        },
        yaxis: {
            title: {
                text: 'العدد'
            }
        },
        legend: {
            position: 'top'
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    position: 'top'
                }
            }
        }
    };

    var userChart = new ApexCharts(document.querySelector("#userChart"), optionsUser);
    userChart.render();
});




// إعدادات الرسم البياني لنسبة المبيعات حسب الفئة
document.addEventListener("DOMContentLoaded", function () {
    // البيانات المستلمة من Flask
    var categories = JSON.parse(document.getElementById("categoriesData").textContent); // أسماء الفئات
    var category_sales = JSON.parse(document.getElementById("categorySalesData").textContent); // مبيعات الفئات

    // إعدادات الرسم البياني
    var optionsCategorySales = {
        chart: {
            type: 'donut',
            height: 350
        },
        series: category_sales,
        labels: categories,
        title: {
            align: 'center',
            style: {
                fontSize: '20px',
                fontWeight: 'bold',
                color: '#000000',
            }
        },
        plotOptions: {
            pie: {
                donut: {
                    size: '65%',
                    labels: {
                        show: true,
                        name: {
                            fontSize: '16px',
                            fontWeight: 600
                        },
                        value: {
                            fontSize: '14px'
                        }
                    }
                }
            }
        },
        dataLabels: {
            enabled: true
        }
    };

    // إنشاء الرسم البياني
    var categorySalesChart = new ApexCharts(document.querySelector("#categorySalesChart"), optionsCategorySales);
    categorySalesChart.render();
});





// إعدادات الرسم البياني لعدد الزيارات
var optionsVisitor = {
    chart: {
        type: 'pie',
        height: 350,
    },
    series: [30, 50, 20],
    labels: ['الزيارات اليومية', 'الزيارات الأسبوعية', 'الزيارات الشهرية'],
    title: {
        text: 'عدد الزيارات'
    }
};
var visitorChart = new ApexCharts(document.querySelector("#visitorChart"), optionsVisitor);
visitorChart.render();

// إعدادات الرسم البياني لأداء البائعين
var optionsSellerPerformance = {
    chart: {
        type: 'radar',
        height: 350,
    },
    series: [{
        name: 'أداء البائعين',
        data: [65, 59, 90, 81, 56]
    }],
    labels: ['البائع 1', 'البائع 2', 'البائع 3', 'البائع 4', 'البائع 5'],
    title: {
        text: 'أداء البائعين'
    }
};
var sellerPerformanceChart = new ApexCharts(document.querySelector("#sellerPerformanceChart"), optionsSellerPerformance);
sellerPerformanceChart.render();



// إعدادات الرسم البياني لنمو المبيعات


document.addEventListener("DOMContentLoaded", function () {
    var salesData = document.getElementById('chartData');
    var monthly = JSON.parse(salesData.getAttribute('data-months'));
    var monthly_sales = JSON.parse(salesData.getAttribute('data-monthly-sales'));

    var optionsSalesGrowth = {
        chart: {
            type: 'bar',
            height: 350,
        },
        series: [{
            name: 'نمو المبيعات',
            data: monthly_sales
        }],
        xaxis: {
            categories: monthly,
            title: {
                text: 'الأشهر'
            }
        },
        yaxis: {
            title: {
                text: 'نمو المبيعات'
            }
        },
        title: {
            text: 'نمو المبيعات حسب الشهر',
            align: 'center',
            style: {
                fontSize: '20px',
                fontWeight: 'bold',
                color: '#000000'
            }
        }
    };

    var salesGrowthChart = new ApexCharts(document.querySelector("#salesGrowthChart"), optionsSalesGrowth);
    salesGrowthChart.render();
});


// إعدادات الرسم البياني لتحليل المنتجات
var optionsProductAnalysis = {
    chart: {
        type: 'donut',
        height: 350,
    },
    series: [300, 50, 100, 70],
    labels: ['المنتج 1', 'المنتج 2', 'المنتج 3', 'المنتج 4'],
    title: {
        text: 'تحليل المنتجات'
    }
};
var productAnalysisChart = new ApexCharts(document.querySelector("#productAnalysisChart"), optionsProductAnalysis);
productAnalysisChart.render();

// إعدادات الرسم البياني لرضا العملاء
var optionsCustomerSatisfaction = {
    chart: {
        type: 'pie',
        height: 350,
    },
    series: [60, 30, 10],
    labels: ['راضي', 'غير راضي', 'محايد'],
    title: {
        text: 'رضا العملاء'
    }
};
var customerSatisfactionChart = new ApexCharts(document.querySelector("#customerSatisfactionChart"), optionsCustomerSatisfaction);
customerSatisfactionChart.render();

// إعدادات الرسم البياني لشعبية المنتجات
var optionsProductPopularity = {
    chart: {
        type: 'donut',
        height: 350,
    },
    series: [40, 30, 20, 10],
    labels: ['المنتج 1', 'المنتج 2', 'المنتج 3', 'المنتج 4'],
    title: {
        text: 'شعبية المنتجات'
    }
};
var productPopularityChart = new ApexCharts(document.querySelector("#productPopularityChart"), optionsProductPopularity);
productPopularityChart.render();
