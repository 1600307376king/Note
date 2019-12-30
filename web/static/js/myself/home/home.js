// 默认分类名称
let labelName = "All";
// 当前页
let currentPage = 2;
// 筛选类型
let filterType = "rec";
// 是否允许加载数据
let is_append = 1;
//请求开关，请求成功后才能再次请求
let requestSwitch = 1;

//左侧下拉菜单
$(function () {
    // nav收缩展开
    $('.navMenu li a').on('click', function () {
        var parent = $(this).parent().parent();//获取当前页签的父级的父级
        var labeul = $(this).parent("li").find(">ul");
        if ($(this).parent().hasClass('open') === false) {
            //展开未展开
            parent.find('ul').slideUp(300);
            parent.find("li").removeClass("open");
            parent.find('li a').removeClass("active").find(".arrow").removeClass("open");
            $(this).parent("li").addClass("open").find(labeul).slideDown(300);
            $(this).addClass("active").find(".arrow").addClass("open")
        } else {
            $(this).parent("li").removeClass("open").find(labeul).slideUp(300);
            if ($(this).parent().find("ul").length > 0) {
                $(this).removeClass("active").find(".arrow").removeClass("open")
            } else {
                $(this).addClass("active")
            }
        }

    });
});

// 右侧顶部菜单筛选
$('.filterCol').on('click', function () {
    let filter = $(this);
    let filterName = filter.attr("value");
    // 删除所有active 对当前添加active
    let filter_list = filter.parent("ul").children();
    for (let i = 0; i < filter_list.length; i++) {
        filter_list[i].classList.remove('active');
    }
    filter[0].classList.add("active");
    filterData(labelName, filterName);
});

// 点击左侧导航菜单筛选
$('.one').on('click', function () {
    is_append = 1;
    let topCategoryName = $(this)[0].childNodes[0].childNodes[0].innerText;
    labelName = topCategoryName;
    filterData(topCategoryName, filterType);
});

// 筛选请求
function filterData(labelName, filterType) {

    $.ajax({
        type: "POST",
        url: "/filter_col/",
        data: JSON.stringify({'filter_type': filterType, "label_name": labelName}),
        dataType: "json",
        headers: {
            'Content-Type': 'application/json',
        },
        success: function (response) {
            is_append = 1;
            currentPage = 2;

            // 删除所有li 并重新添加li
            let liOneNotes = document.getElementsByClassName("one_notes");
            let notes = document.getElementsByClassName("notes")[0];
            let count = liOneNotes.length;
            let copyData = liOneNotes[0].cloneNode(true);

            for (let k = 0; k < count; k++) {
                notes.removeChild(liOneNotes[0]);
            }
            let responseData = response.note_msg;
            for (let j = 0; j < responseData.length; j++) {
                let cloneData = copyData.cloneNode(true);
                if (responseData[j][1].length > 50) {
                    responseData[j][1] = responseData[j][1].substring(0, 50) + '...'
                }
                // 修改标题名称
                cloneData.childNodes[1].childNodes[1].childNodes[1].innerText = responseData[j][1];

                //修改标签名称
                let labelList = responseData[j][2].split('|');
                for (let m = 0; m < labelList.length - 1; m++) {
                    let index = (m + 1) * 2 - 1;
                    if (cloneData.childNodes[1].childNodes[3].childNodes[3].childNodes[index] === undefined) {
                        cloneData.childNodes[1].childNodes[3].childNodes[3].appendChild(document.createElement("span"));
                    }
                    cloneData.childNodes[1].childNodes[3].childNodes[3].childNodes[index].innerText = labelList[m];
                }
                // 阅读数
                cloneData.childNodes[1].childNodes[3].childNodes[5].childNodes[3].innerText = responseData[j][4];
                notes.append(cloneData);
            }
        }
    })
}

// 向下滚动加载数据
function roll() {
    let listObj = $(".notes");
    let domHeight = document.getElementsByClassName("notes")[0];
    // note列表数据动态加载
    if (domHeight.scrollHeight - 100 < listObj.scrollTop() + domHeight.clientHeight) {

        if ($(".sort_note ul .active")[0].innerText === '最新添加') {
            filterType = "new";
        }
        setTimeout(get_data, 500);
    }
}

function get_data() {
    if (is_append !== -1 && requestSwitch === 1) {
        requestSwitch = -1;
        document.getElementById("loadTipBlock").style.opacity = "100";
        $.ajax({
            type: "GET",
            url: "/load_data/" + "?page=" + currentPage + "&type=" + filterType + "&label=" + labelName,
            success: function (response) {
                if (response.msg === 'continue') {
                    if (response.warning === 'break' || currentPage === parseInt(response.cur_num)) {
                        is_append = -1
                    }
                    currentPage = response.cur_num;
                    let liOneNotes = document.getElementsByClassName("one_notes");
                    let notes = document.getElementsByClassName("notes")[0];
                    let copyData = liOneNotes[0].cloneNode(true);
                    let responseData = response.res;
                    for (let j = 0; j < responseData.length; j++) {
                        let cloneData = copyData.cloneNode(true);
                        // 标题
                        if (responseData[j][1].length > 50) {
                            responseData[j][1] = responseData[j][1].substring(0, 50) + '...'
                        }
                        cloneData.childNodes[1].childNodes[1].childNodes[1].innerText = responseData[j][1];
                        //标签
                        let labelList = responseData[j][2].split('|');
                        for (let m = 0; m < labelList.length - 1; m++) {
                            let index = (m + 1) * 2 - 1;
                            if (cloneData.childNodes[1].childNodes[3].childNodes[3].childNodes[index] === undefined) {
                                cloneData.childNodes[1].childNodes[3].childNodes[3].appendChild(document.createElement("span"));
                            }
                            cloneData.childNodes[1].childNodes[3].childNodes[3].childNodes[index].innerText = labelList[m];
                        }
                        // 阅读数
                        cloneData.childNodes[1].childNodes[3].childNodes[5].childNodes[3].innerText = responseData[j][4];
                        notes.appendChild(cloneData);
                    }
                    requestSwitch = 1;
                    document.getElementById("loadTipBlock").style.opacity = "0";
                }
            },
            complete: function () {
                document.getElementById("loadTipBlock").style.opacity = "0";
            }
        })
    }
}