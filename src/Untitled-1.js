try {
    if (pageModel.cust.custDic[imgType].value !== '' && pageModel.cust.custDic[imgType].value !== null) {
        imgSrc = pageModel.cust.custDic[imgType].value;
    } else {
        try {
            imgSrc = pageModel.pc.common.bannerImage ? pageModel.pc.common.bannerImage : "";
        } catch (err) {
            console.log(err);
        }
    }
} catch (err) {
    try {
        imgSrc = pageModel.pc.common.bannerImage ? pageModel.pc.common.bannerImage : "";
    } catch (err) {
        console.log(err);
    }
}


//====
imgSrc = "";
isCustDicValue = false;
isBannerImage =false;

try{
    isCustDicValue = !!pageModel.cust.custDic[imgType].value;
}catch(e){
    console.log(e)
}finally{
    if(isCustDicValue)
        imgSrc = pageModel.cust.custDic[imgType].value;
    else
        try{
            isBannerImage = !!pageModel.pc.common.bannerImage;
        }catch(e){
            console.log(e)
        }

        if(isBannerImage)
            imgSrc = pageModel.pc.common.bannerImage;
        else
            imgSrc = "";
}












imgSrc = 'none';
try{
    imgSrc = pageModel.cust.custDic[imgType].value;
}catch{
    imgSrc = 'err'
}finally{
    
    if (imgSrc == 'err')
        try{
            imgSrc = pageModel.pc.common.bannerImage
        }catch{
            imgSrc = 'err'
        }
}

if(typeof imgSrc == 'undefined' || imgSrc == null)
    imgSrc = ""


    