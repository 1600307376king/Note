
/*---------------------下拉菜单单选、复选组建---------------------*/
;(function($){
	$.fn.multiSelect=function(options){
		var defaults = {
			selectedHtmlValue: '请选择',
			titleEventType: 'click',
			optionEventType: 'click',
			selectedIcon: '<i class="fa fa-check arrow"></i>',
			selectedProperty: 'data-select',
			multiple: true,
			setWidth: '150px',
			setMaxOptionNum: 8,
			optionsHoverStyle: 'newOptions_hover',      
			change: function(){},
			mutiConfEvent:function(){}
		};
		
		var options = $.extend(defaults,options);
	
		this.each(function(){
			var _tDom = this,_t = $(_tDom);
			var _thisHtmlValue,_thisValue,newSelect,newSelectTitle,selectedOption = '',newOptions = '',selected = '',sArea,newOptionsHeight,titleText = '';
			
			//判断是否已经执行过此方法
			if(_t.next().is('div.newSelect')){
				_t.next().remove();
			}
			
			//遍历原来select中option标签
			_t.find('option').each(function(i){
				var _this = $(this);
				_thisHtmlValue = _this.html().substr(0,options.setMaxOptionNum);
				_thisValue = _this.val();
				
				if(_t.attr('data-default') == _thisValue){
					_this.attr(options.selectedProperty,true);
				}
				//_t.after(_t.attr(options.selectedProperty));
				
				if(options.multiple){

					if(_this.attr(options.selectedProperty)){
						selectedOption = 'data-select="true"';
						selected = options.selectedIcon;
						titleText += _this.html()+',';
					}else{
						selectedOption = '';
						selected = '';
						
					}
					
				}else{
					
					if(_this.attr(options.selectedProperty)){
						selectedOption = 'data-select="true"';
						titleText = _this.html();
					}else{
						selectedOption = '';
						selected = '';
						
					}
					
				}
					
					
					newOptions += "<li data-value='"+_thisValue+"' "+ selectedOption +" >"+ _thisHtmlValue + selected +"</li>";								// 创建新的options
				
				
			});
			
			var a = titleText?titleText:options.selectedHtmlValue;
			
			newSelectTitle = '<lable class="newSelectTitle"><span>'+a+'</span><i class="fa fa-angle-down arrow"></i></lable>';			// 创建新的selectTitle
			
			sArea = (options.multiple)?'<li class="sArea"><button onclick="javascript:return false;" value="确定">确定</button></li>':'';
			
			newOptionsHeight = options.setMaxOptionNum * 30;
			
			newOptions = '<ul class="newOptions" style="width:'+options.setWidth+';max-height:' + newOptionsHeight + 'px;overflow-y:auto;">'+newOptions+sArea+'</ul>';
			
			newSelect = '<div class="newSelect" style="width:'+options.setWidth+';">'+newSelectTitle+newOptions+'</div>';			// 创建新的select
			
			
			
			_t.css('display','none').after(newSelect);
			
			
			//select标题绑定点击事件
			var optionSwitch = 0,_thisNewSelect = _t.next(),n_o,_p;
			_thisNewSelect.find('.newSelectTitle').on(options.titleEventType,function(){
				var n_o = $(this).next('.newOptions'),_p = $(this).find('i.arrow'),_t = $(this);
				
				if(optionSwitch){
					
					_p.removeClass('arrow_turn');
					n_o.slideUp("fast",function(){
						optionSwitch = 0;
					});
					
				}else{
					
					_p.addClass('arrow_turn');
					n_o.slideDown("fast",function(){
						optionSwitch = 1;
						
						$(document).one(options.titleEventType,function(event){
							var target_p = $(event.target).parents('.newSelect');
							if(target_p.html() != _thisNewSelect.html()){
								_p.removeClass('arrow_turn');
								n_o.slideUp("fast",function(){
									optionSwitch = 0;
								});
							}
						});
					});
				}
			});
			
			
			
			//select内option绑定点击事件
			_thisNewSelect.find('.newOptions li').on(options.optionEventType,function(){
				var thisLi = $(this);
				var thisIndex = _thisNewSelect.find('.newOptions li').index(thisLi);
				//判断是否多选
				if(!options.multiple){
					_thisNewSelect.find('.newSelectTitle span').html(thisLi.html());
					_thisNewSelect.find('.newSelectTitle').trigger(options.titleEventType);

					if(!thisLi.attr(options.selectedProperty)){
						_thisNewSelect.find('.newOptions li').removeAttr(options.selectedProperty);
						_t.find('option['+options.selectedProperty+'="true"]').removeAttr(options.selectedProperty);
						add.call(_t.find('option').eq(thisIndex));
						options.change.call(_t.find('option['+options.selectedProperty+'="true"]'));
					}

				}else{
					//多选
					if(!thisLi.attr(options.selectedProperty)){
						thisLi.append(options.selectedIcon);
						add.call(_t.find('option['+options.selectedProperty+'="true"]'));
					}else{
						thisLi.removeAttr(options.selectedProperty);
						_t.find('option').eq(thisIndex).removeAttr(options.selectedProperty);
						thisLi.find('i.fa').remove();
					}
				}

				function add(){
					_t.find('option').eq(thisIndex).attr(options.selectedProperty,true);
					thisLi.attr(options.selectedProperty,true);
				}
				
				
				return false;
			});
			
			
			if(options.multiple){
				//解除绑定确认栏点击事件
				_thisNewSelect.find('.sArea').off(options.optionEventType);
				

				_thisNewSelect.find('.sArea button').on('click',function(event){
					var divValue = '',textVal = '',selectLi = $(this).parents('ul.newOptions').find('li['+options.selectedProperty+'="true"]');

					if(selectLi.length > 0){
						selectLi.each(function(){
							var _pi = $(this).find('i');
							_pi.remove();
							divValue += $(this).html()+',';
							$(this).append(_pi);
						});
						_thisNewSelect.find('.newSelectTitle span').html(divValue);
					}else{
						_thisNewSelect.find('.newSelectTitle span').html(options.selectedHtmlValue);
					}
					
					_thisNewSelect.find('.newSelectTitle i.arrow').removeClass('arrow_turn');
					_thisNewSelect.find('.newOptions').slideUp("fast",function(){optionSwitch = 0;});
					
					options.mutiConfEvent.call(_tDom);
					//return false;
				});
			}
			
		});
	};
	
	
})(jQuery);


