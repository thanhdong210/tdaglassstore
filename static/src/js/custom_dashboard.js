odoo.define("custom_dashboard.DashboardDashboard", function (require) {
    "use strict";
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var QWeb = core.qweb;
    var web_client = require('web.web_client');
    var session = require('web.session');
    var ajax = require('web.ajax');
    var _t = core._t;
    var rpc = require('web.rpc');
    var self = this;
    var utils = require('web.utils');

    var DashBoard = AbstractAction.extend({
        contentTemplate: 'DashboardDashboard',

        template: "DashboardDashboard",
        jsLibs: [
            '/web/static/lib/Chart/Chart.js',
        ],

        init: function(parent, context) {
            this._super(parent, context);
            this.dashboard_templates = ['MainSection', 'MainSection2'];
            this.chart = null;
            this.chartId =  _.uniqueId('chart_example');
        },
        start: function() {
            var self = this;
            this.set("title", 'Dashboard');
            return this._super().then(function() {
                self.render_dashboards();
            });
        },
        willStart: function(){
            var self = this;
            return this._super()
        },
        render_dashboards: function() {
            var self = this;
            this.fetch_data()
            var templates = []
            var templates = ['MainSection', 'MainSection2'];
            _.each(templates, function(template) {
                self.$('.o_hr_dashboard').append(QWeb.render(template, {widget: self}))
            });

            this.people_visit_site_chart()
            this.product_by_category_chart()
            this.product_clicked_chart_line()
        },

        people_visit_site_chart: function() {
            var canvas = this.$('canvas')[0];
            var newWidth = 857;
            var newHeight = 200;
            var data = {
                labels: ['Label 1', 'Label 2', 'Label 3'],
                datasets: [{
                    label: 'My First Dataset',
                    data: [10, 20, 30],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                    ],
                    borderWidth: 1
                }]
            }
            var options = {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                responsive: true,
                maintainAspectRatio: true
            }
            this.render_chart(canvas, 'bar', data, options, newWidth, newHeight)
        },

        product_by_category_chart: function() {
            var canvas = this.$('canvas')[1];
            var newWidth = 857;
            var newHeight = 200;
            var self = this

            var labels = []
            var data = []

            var def1 = this._rpc({
                model: 'tda.product.product',
                method: "get_product_by_category",
            })
            .then(function (result) {
                labels = result.categories_name
                data = result.categories_count

                var data = {
                    labels: labels,
                    datasets: [{
                        label: "Category's product",
                        data: data,
                        backgroundColor: [
                            'rgb(255, 99, 132)',
                            'rgb(54, 162, 235)',
                            'rgb(255, 205, 86)'
                            ],
                        hoverOffset: 4
                    }]
                }
                var options = {}
                self.render_chart(canvas, 'pie', data, options, newWidth, newHeight)
            });
        },

        addMonths: function(d,n){
            // var full_month = ["January","February","March","April","May","June","July","August","September","October","November","December"];
            var dt = new Date(d.getTime());
            dt.setMonth(dt.getMonth()+n);
            const month = dt.toLocaleString('default', { month: 'long' });
            return month;
        },

        product_clicked_chart_line: function() {
            var canvas = this.$('canvas')[2];
            var labels = []
            var data = []
            var newWidth = 3000;
            var newHeight = 400;
            var self = this

            var def1 = this._rpc({
                model: 'tda.advisory.request',
                method: "get_advisory_request_by_month",
            })
            .then(function (result) {
                labels = result.last_7_month_name
                data = result.last_7_month_count

                var data = {
                    labels: labels,
                    datasets: [{
                        label: 'My First Dataset',
                        data: data,
                        fill: false,
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1
                    }]
                };
                var options = {}
                self.render_chart(canvas, 'line', data, options, newWidth, newHeight)
            });
            
        },

        render_chart: function(canvas, type, data, options, newWidth, newHeight) {
            var ctx = canvas.getContext('2d');
            var myChart = new Chart(ctx, {
                type: type,
                data: data,
                options: options
            });

            var newWidth = newWidth;  // Set your new width
            var newHeight = newHeight; // Set your new height

            // Update canvas attributes
            // canvas.width = newWidth;
            // canvas.height = newHeight;

            // Get chart context and update the chart
            myChart.config.options.maintainAspectRatio = false; // Allow resizing
            myChart.update();
        },

        fetch_data: function() {
            var self = this
    //          fetch data to the tiles
            var def1 = this._rpc({
                model: 'tda.product.product',
                method: "get_data",
            })
            .then(function (result) {
                $('#products').append('<span>' + result.products + '</span>');
                $('#categories').append('<span>' + result.categories + '</span>');
            });
        },

        
    });
    core.action_registry.add('custom_dashboard_tag', DashBoard);
    return DashBoard;
 });