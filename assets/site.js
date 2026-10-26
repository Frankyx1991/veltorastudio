"use strict";
const search=document.querySelector('[data-search]');
if(search){
 const cards=[...document.querySelectorAll('[data-search-text]')];
 const count=document.querySelector('[data-count]');
 const empty=document.querySelector('[data-empty]');
 const singular=search.dataset.kind==='aplicaciones'?'aplicación':'juego';
 const plural=search.dataset.kind==='aplicaciones'?'aplicaciones':'juegos';
 const clean=value=>value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase('es');
 search.addEventListener('input',()=>{
  const query=clean(search.value.trim());let visible=0;
  for(const card of cards){card.hidden=!clean(card.dataset.searchText).includes(query);if(!card.hidden)visible++;}
  count.textContent=`${visible} ${visible===1?singular:plural}`;
  empty.hidden=visible>0;
 });
}
