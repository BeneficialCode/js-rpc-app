function getRandomInteger(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function ol(arg){
    let e = arg.length;
    var t = [[getRandomInteger(-1,1),0,getRandomInteger(110,150)]]
    var x,y,t;
    for (let index = 1; index < (e-1); index++) {
        if(index == 1){
            t.push([getRandomInteger(-1,1),getRandomInteger(-1,1),getRandomInteger(1,6)]);
        }else{
            var oo =(arg[index][2] - arg[index-1][2]) ;
            var cc = (arg[index][1] - arg[index-1][1])
            t.push( [(arg[index][0] - arg[index-1][0]),cc,oo]);
        }
    }
    t.push([0,0,getRandomInteger(250,300)])
    return t;
}

function getslidetrack(x) {
    let x_ = getRandomInteger(10, 45);
    let y_ = getRandomInteger(10, 45);
    var x1 = 0, t1 = 0, x2 = 0, t2 = 0, i = 0, track = [], yi = 0, t = 0;
    track.push([-1 * x_, -1 * y_, 0]), track.push([0, 0, 0]);
    x_ = y_ = 0;
    var x1arr = [1, 3, 2, 1, 2, 1, 3, 1, 4, 1],
        t1arr = [1, 0, 1, 3, 1],
        x2arr = [1, 2, 1, 0, 1, 2, 1],
        x1arr1 = [2, 3, 1, 3, 2, 1, 1],
        t1arr1 = [1, 0, 3, 2, 1, 4],
        x2arr1 = [1, 2, 1, 0, 1, 2, 1],
        x2arr2 = [2, 1, 2, 1, 2, 1, 1, 3],
        x2arr3 = [1, 1, 0, 1, 0, 1, 1, 2],
        yarr = [0, 0, 0, 1, 1, 1, -1, -1, -1];
    var key;
    while (x_ < x) {
        i++;
        (x - x_ < 13) && (key = 2) || (x - x_ < 5) && (key = 3) || (x > 100 ? key = 0 : key = 1);
    
        switch (key) {
            case 0:
                x1 = x1arr[getRandomInteger(0, x1arr.length - 1)];
                t1 = t1arr[getRandomInteger(0, t1arr.length - 1)];
                x2 = x2arr[getRandomInteger(0, x2arr.length - 1)];
                t2 = getRandomInteger(10, 22)
                break;
            case 1:
                x1 = x1arr1[getRandomInteger(0, x1arr1.length - 1)];
                t1 = t1arr1[getRandomInteger(0, t1arr1.length - 1)];
                x2 = x2arr1[getRandomInteger(0, x2arr1.length - 1)];
                t2 = getRandomInteger(17, 25)
                break;
            case 2:
                x1 = 1;
                t1 = getRandomInteger(10, 22);
                x2 = x2arr2[getRandomInteger(0, x2arr2.length - 1)];
                t2 = getRandomInteger(17, 28)
                break;
            case 3:
                x1 = 1;
                t1 = getRandomInteger(60, 85);
                x2 = x2arr3[getRandomInteger(0, x2arr3.length - 1)];
                t2 = getRandomInteger(60, 85)
                break;
            default:
                break;
        }
        if (yi < 5) {
            if (yi == 1) {
                y_ += [0, 0, 0, 1, 1, 1, -1, -1, -1][getRandomInteger(0, 8)]
            }
            yi++;
        } else {
            yi = 0
        }
        track.push([x_ += x1, y_, t += t1]);
        track.push([x_ += x2, y_, t += t2])
    }
    track.push([x_ += getRandomInteger(-1, 1), y_, t += getRandomInteger(100, 300)]);
    return track
}

function get_actoken(x,y,token){
    dxinit=window._dx.UA.init({"token":token});
    //初始化生成第一段UA
    dxinit.start()
    //初始化各自检测
    //这个是按下
    document.implementation = {
        hasFeature : function(a,b){return true}
    };

    let e = {button:0,pageX:getRandomInteger(10,40),pageY:getRandomInteger(10,40)}

    dxinit['getMD'](e)

    //这个是滑动
    let guiji = ol(getslidetrack(x));
    for (let index = 0; index < guiji.length; index++) {
        e.pageX += guiji[index][0];
        e.pageY += guiji[index][1];
        dxinit['recordSA'](e)
    }
    dxinit.sendSA();
    //这里是省sendSA 填充UA
    dxinit.sendTemp('x=' + (x) + '&y=' + y)
    //传入距离 生成最后一段UA
    return dxinit.getUA();
}