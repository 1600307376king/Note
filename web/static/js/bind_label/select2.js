(function($, window, document, undefined) {
    var MySelect = function(element, options) {
        this.$element = $(element);
        let className = $.trim(this.$element.attr("class")).split(" ") || [];
        this.$el = "." + className.join(".");
        this.options = $.extend({}, $.fn.mySelect.defaults, options, this.$element.data());
        this._init();
    };
    MySelect.prototype = {
        constructor: MySelect,
        _init: function() {
            this.$template = $($.fn.mySelect.template);
            this.$templateItem = $($.fn.mySelect.templateItem);
            this.$element.append($("<style></style>"));
            this.$element.append(this.$template);
            this.$style = this.$element.find("style");
            this.$search = $(this.$template[0]);
            this.$wrp = $(this.$template[1]);
            this.$select = this.$element.find("select");
            this.$options = this.$select.find("option");
            this.$searchBar = this.$wrp.find('.select-picker-options-serch');
            this.$optionList = this.$template.find(".select-picker-options-list");
            this.$emptyList = this.$template.find(".select-picker-options-list-alert");
            this._showSearch();
            this._drawList();
            this.$search.click($.proxy(this._showList, this));
            this.$optionList.delegate(".select-picker-options-list-item", "click", $.proxy(this._check, this));
            this._initChoose();
            this._setChooseText();
            this._showCancel();
        },
		_initChoose: function() {
			var self = this;
            var checks = this.$element.data("checks")||null;
            if(checks){
            	var list = checks.split(",");
            	$(list).each(function(i, val) {
                    self.$optionList.find(".select-picker-options-list-item[data-val=" + val + "]"+" .duihao").removeClass('duihao-nocheck').addClass('duihao-checked');
            	});
            	this._isAll();
            }
        },
        _isJSON: function(str) {
            if (typeof str == 'string') {
		        try {
		            var obj=JSON.parse(str);
		            if(typeof obj == 'object' && obj ){
		                return true;
		            }else{
		                return false;
		            }
		        } catch(e) {
		            return false;
		        }
		    }
        },
        _getOptionDatas: function() {
            var result = [];
            if (this.$element.data("init")) {
            	var dataArr = null;
                if (this._isJSON(this.$element.data("init"))) {
                	result = JSON.parse(this.$element.data("init"));
                }else{
                	dataArr = this.$element.data("init").toString().split(",");
	                $(dataArr).each(function(i, val) {
	                    var map = {
	                        val: val || "",
	                        text: val || "",
	                    }
	                    result.push(map);
                	});
                }
            } else {
                this.$options.each(function() {
                    var _this = $(this);
                    var map = {
                        val: _this.val() || "",
                        text: _this.text() || "",
                    }
                    result.push(map);
                });
            }
            if (this.options.isSort) {
                result.sort(this._sortText);
            }
            if (result.length > 0 && this.options.multiple) {
                var text = this.options.model ? "All " + this.options.model : "All";
                result.unshift({
                    val: "ALL",
                    text: text,
                });
            }
            return result;
        },
        _sortText: function(a, b) {
            return a.text - b.text
        },
        _drawList: function() {
            var self = this;
            self.$optionList.empty();
            if (self._getOptionDatas().length > 0) {
                $(self._getOptionDatas()).each(function() {
                    var $tmp = self.$templateItem.clone();
                    $tmp.find("span").html(this.text);
                    $tmp.attr("data-val", this.val);
                    if (this.val == "ALL") {
                        $tmp.addClass('chooseAll');
                    }
                    self.$optionList.append($tmp);
                });
            } else {
                self._showEmpty(true);
            }
        },
        /*
         * toggles show/hide
         */
        _showList: function() {
            this.$search.toggleClass("open");
            this.$wrp.find('.select-picker-options-serch input').focus();
        },
        _showSearch: function() {
            var self = this;
            self.$searchBar.addClass("hidden");
            if (self.options.showSearch) {
                self.$searchBar.removeClass("hidden");
                self.$searchBar.find("input").bind('input propertychange', function() {
                    var keyword = this.value;
                    self._search(keyword);
                });
            }
        },
        _showCancel: function() {
            this.$wrp.find('.select-picker-btn-group').addClass("hidden");
            if (this.options.showCancel) {
                this.$wrp.find('.select-picker-btn-group').removeClass("hidden");
                var self = this;
                this.$wrp.find('.select-picker-btn-group .select-picker-btn-cancel').click(function(e) {
                    self._emptyAll();
                    self._setChooseText();
                    self.$search.removeClass("open");
                });
            }
        },
        _search: function(keyword) {
            keyword = (keyword || '').toLowerCase();
            let self = this,
                selectorBuffer = [],
                groupIndex = -1,
                itemCount = 0,
                liArray = this.$optionList.find(".select-picker-options-list-item"),
                itemTotal = liArray.length;
            var checkGroup = function(currentIndex, last) {
                if (itemCount >= (currentIndex - groupIndex - (last ? 0 : 1))) {
                    selectorBuffer.push(self.$el + ' .select-picker-options-list .select-picker-options-list-item:nth-child(' + (groupIndex + 1) + ')');
                };
                groupIndex = currentIndex;
                itemCount = 0;
            }
            liArray.each(function(index, item) {
                var currentIndex = index;
                var text = (item.innerText || '').toLowerCase();
                if (keyword && text.indexOf(keyword) < 0) {
                    selectorBuffer.push(self.$el + ' .select-picker-options-list .select-picker-options-list-item:nth-child(' + (currentIndex + 1) + ')');
                    itemCount++;
                }
                if (currentIndex >= (itemTotal - 1)) {
                    checkGroup(currentIndex, true);
                }
            });
            if (selectorBuffer.length >= itemTotal) {
                self._showEmpty(true);
                self.$style.text(selectorBuffer.join(', ') + "{display:none;}");
            } else if (selectorBuffer.length > 0) {
                self._showEmpty(false);
                self.$style.text(selectorBuffer.join(', ') + "{display:none;}");
            } else {
                self._showEmpty(false);
                self.$style.text("");
            }
        },
        _showEmpty: function(isShow) {
            this.$emptyList.addClass("hidden");
            if (isShow) {
                this.$emptyList.removeClass("hidden");
            }
        },
        _check: function(e) {
            let _this = $(e.currentTarget);
            if (_this.is(".chooseAll")) {
                if (_this.find('.duihao-nocheck').length > 0) {
                    this._checkAll();
                } else {
                    this._emptyAll();
                }
            } else {
                if (this.options.multiple) {
                    if (_this.find('.duihao-nocheck').length > 0) {
                        _this.find('.duihao').removeClass('duihao-nocheck').addClass('duihao-checked');
                    } else {
                        _this.find('.duihao').addClass('duihao-nocheck').removeClass('duihao-checked');
                    }
                    this._isAll();
                } else {
                    if (_this.find('.duihao-nocheck').length > 0) {
                        this._emptyAll();
                        _this.find('.duihao').removeClass('duihao-nocheck').addClass('duihao-checked');
                    } else {
                        _this.find('.duihao').addClass('duihao-nocheck').removeClass('duihao-checked');
                    }
                    this.$search.removeClass("open");
                }
            }
            this._setChooseText();
        },
        _isAll: function() {
            let $left = this.$optionList.find(".select-picker-options-list-item .duihao-nocheck");
            if ($left && $left.length == 1) {
                let $parent = $($left[0]).parent();
                if ($parent.is(".chooseAll")) {
                    $left.removeClass('duihao-nocheck').addClass('duihao-checked');
                } else {
                    this.$optionList.find(".select-picker-options-list-item.chooseAll .duihao").addClass('duihao-nocheck').removeClass('duihao-checked');
                }
            }
        },
        _emptyAll: function() {
            this.$optionList.find(".select-picker-options-list-item .duihao").addClass('duihao-nocheck').removeClass('duihao-checked');
        },
        _checkAll: function() {
            this.$optionList.find(".select-picker-options-list-item .duihao").removeClass('duihao-nocheck').addClass('duihao-checked');
        },
        _getCheckedValue: function() {
            let checkedArr = [],
                checkedArrValue = [],
                isAll = false;
            this.$optionList.find(".select-picker-options-list-item").each(function() {
                if ($(this).find('.duihao-checked').length > 0) {
                    if ($(this).is(".chooseAll")) {
                        isAll = true;
                    } else {
                        let text = $.trim($(this).text()),
                            val = $.trim($(this).data("val")) || null;
                        checkedArr.push(text);
                        checkedArrValue.push(val);
                    }
                }
            });
            return {
                texts: checkedArr,
                vals: checkedArrValue,
                isAll: isAll
            };
        },
        _setChooseText: function() {
            let checks = this._getCheckedValue();
            let texts = checks.texts || [];
            if (texts.length > 0) {
                this.$template.find('.select-picker-search-checked').text(texts.join(','));
                this.$element.data("val", checks.vals);
                this.$element.data("isAll", checks.isAll);
            } else {
                this.$template.find('.select-picker-search-checked').text('Please Select');
                this.$element.data("val", "");
                this.$element.data("isAll", false);
            }
        }
    }
    $.fn.mySelect = function(options) {
        var args = Array.apply(null, arguments);
        args.shift();
        this.each(function() {
            var $this = $(this),
                data = $this.data('mySelect');
            if (data) $this.data('mySelect').remove();
            $this.data('mySelect', new MySelect(this, options));
        });
    }
    $.fn.mySelect.defaults = {
        showCancel: false,
        showSearch: false,
        multiple: false,
        isSort: true
    };
    $.fn.mySelect.template = '' + '<div class="select-picker-search">' + '<div class="select-picker-search-checked"></div>' + '</div>' + '<div class="select-picker-options-wrp">' + '<div class="select-picker-options-serch">' + '<input type="text" placeholder="">' + '</div>' + '<div class="select-picker-options-list"></div>' + '<div class="select-picker-options-list-alert hidden">No Content</div>' + '<div class="select-picker-btn-group">' + '<div class="select-picker-btn-cancel">Cancel</div>' + '</div>' + '</div>';
    $.fn.mySelect.templateItem = '' + '<div class="select-picker-options-list-item">' + '<b class="duihao duihao-nocheck"></b>' + '<span></span>' + '</div>';
    $(document).click(function(event) {
        var _con = $('.select-picker-options-wrp');
        var _con2 = $('.select-picker-search-checked');
        if (!_con2.is(event.target) && !_con.is(event.target) && _con.has(event.target).length === 0) {
            $('.select-picker-search').removeClass("open");
        }
    });
})(jQuery, window, document);