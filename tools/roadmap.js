// Общий модуль: слайд «Где мы и сколько осталось».
// Вставляется вторым слайдом в каждую колоду курса, сразу после титульного.
const BLUE='005AAA', DEEP='1E4270', ACC='9E4257', INK='1E293B', MUTE='64748B',
      LIGHT='F5F7FA', LINE='D8DEE6', W='FFFFFF', F='Arial';
const M=0.55, CW=10-2*M;

// Четыре вехи курса, на каждой команда предъявляет материальный результат.
const VEHI=[
 {d:'26.09',t:'Тема зафиксирована',r:'Паспорт проекта\n+ представление, 3 минуты'},
 {d:'24.10',t:'План собран',r:'WBS, график Ганта,\nсмета и реестр рисков'},
 {d:'21.11',t:'Чекпоинт',r:'Промежуточный результат\n+ сверка «план против факта»'},
 {d:'26.12',t:'Питч-защита',r:'Готовый результат,\nотчёт и защита перед комиссией'}];

const TESTY='Зачётные тесты:  10.10 — тест 1 «Инициация»   ·   28.11 — тест 2 «Планирование и контроль»';

// cfg: {here: индекс ближайшей вехи (0..3), countdown: строка обратного отсчёта, num, total}
function addRoadmap(pres, cfg){
  const s=pres.addSlide(); s.background={color:W};
  s.addText(cfg.num+' / '+cfg.total,{x:10-M-1.2,y:5.2,w:1.2,h:0.26,isTextBox:true,margin:0,
    fontFace:F,fontSize:10,color:MUTE,align:'right'});
  s.addText('ГДЕ МЫ И СКОЛЬКО ОСТАЛОСЬ',{x:M,y:0.2,w:CW,h:0.24,isTextBox:true,margin:0,
    fontFace:F,fontSize:11,color:MUTE,charSpacing:1.5});
  s.addText('Дорожная карта курса',{x:M,y:0.4,w:CW,h:0.62,isTextBox:true,margin:0,
    fontFace:F,fontSize:26,bold:true,color:BLUE});

  // полоса обратного отсчёта
  s.addShape(pres.ShapeType.roundRect,{x:M,y:1.1,w:CW,h:0.62,rectRadius:0.05,
    fill:{color:DEEP},line:{color:DEEP,width:0.5}});
  s.addText(cfg.countdown,{x:M+0.25,y:1.2,w:CW-0.5,h:0.42,isTextBox:true,margin:0,
    fontFace:F,fontSize:14,bold:true,color:W,align:'center',valign:'middle'});

  // линия времени
  s.addShape(pres.ShapeType.rect,{x:M+0.15,y:2.12,w:CW-0.3,h:0.035,fill:{color:LINE},line:{width:0}});

  const gap=0.16, cw=(CW-3*gap)/4;
  VEHI.forEach((v,i)=>{
    const x=M+i*(cw+gap), hot=(i===cfg.here);
    s.addShape(pres.ShapeType.ellipse,{x:x+cw/2-0.09,y:2.0,w:0.18,h:0.18,
      fill:{color:hot?ACC:BLUE},line:{color:W,width:1.5}});
    s.addShape(pres.ShapeType.roundRect,{x,y:2.35,w:cw,h:1.85,rectRadius:0.05,
      fill:{color:hot?DEEP:LIGHT},line:{color:hot?DEEP:LINE,width:0.75}});
    s.addText(v.d,{x:x+0.12,y:2.48,w:cw-0.24,h:0.32,isTextBox:true,margin:0,
      fontFace:F,fontSize:17,bold:true,color:hot?W:BLUE,align:'center'});
    s.addText(v.t,{x:x+0.12,y:2.82,w:cw-0.24,h:0.32,isTextBox:true,margin:0,
      fontFace:F,fontSize:12.5,bold:true,color:hot?W:INK,align:'center'});
    s.addText(v.r,{x:x+0.1,y:3.2,w:cw-0.2,h:0.9,isTextBox:true,margin:0,
      fontFace:F,fontSize:10.5,color:hot?'DCE6F0':MUTE,align:'center',lineSpacing:14});
  });
  s.addText('▲ вы здесь',{x:M+cfg.here*(cw+gap),y:1.78,w:cw,h:0.22,isTextBox:true,margin:0,
    fontFace:F,fontSize:10.5,bold:true,color:ACC,align:'center'});

  s.addShape(pres.ShapeType.roundRect,{x:M,y:4.35,w:CW,h:0.58,rectRadius:0.05,
    fill:{color:LIGHT},line:{color:LINE,width:0.75}});
  s.addText(TESTY,{x:M+0.2,y:4.44,w:CW-0.4,h:0.4,isTextBox:true,margin:0,
    fontFace:F,fontSize:12,color:INK,align:'center',valign:'middle'});

  s.addNotes('Слайд показывается на каждом занятии. Смысл: студент всё время видит, сколько осталось и что именно он обязан предъявить на ближайшей вехе. Отсчёт называть вслух — это и есть встроенный тайм-менеджмент, без отдельной лекции про него.');
  return s;
}
module.exports={addRoadmap, VEHI};
