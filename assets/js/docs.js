"use strict";


/* ====== Define JS Constants ====== */
const sidebarToggler = document.getElementById('docs-sidebar-toggler');
const sidebar = document.getElementById('docs-sidebar');
const sidebarLinks = document.querySelectorAll('#docs-sidebar .scrollto');



/* ===== Responsive Sidebar ====== */

window.onload=function() 
{ 
    responsiveSidebar(); 
};

window.onresize=function() 
{ 
    responsiveSidebar(); 
};


function responsiveSidebar() {
    let w = window.innerWidth;
	if(w >= 1200) {
	    // if larger 
	    console.log('larger');
		sidebar.classList.remove('sidebar-hidden');
		sidebar.classList.add('sidebar-visible');
		
	} else {
	    // if smaller
	    console.log('smaller');
	    sidebar.classList.remove('sidebar-visible');
		sidebar.classList.add('sidebar-hidden');
	}
};

sidebarToggler.addEventListener('click', () => {
	if (sidebar.classList.contains('sidebar-visible')) {
		console.log('visible');
		sidebar.classList.remove('sidebar-visible');
		sidebar.classList.add('sidebar-hidden');
		
	} else {
		console.log('hidden');
		sidebar.classList.remove('sidebar-hidden');
		sidebar.classList.add('sidebar-visible');
	}
});


/* ===== Smooth scrolling ====== */
/*  Note: You need to include smoothscroll.min.js (smooth scroll behavior polyfill) on the page to cover some browsers */
/* Ref: https://github.com/iamdustan/smoothscroll */

sidebarLinks.forEach((sidebarLink) => {
	
	sidebarLink.addEventListener('click', (e) => {
		
		e.preventDefault();
		
		var target = sidebarLink.getAttribute("href").replace('#', '');
		
		//console.log(target);
		
        document.getElementById(target).scrollIntoView({ behavior: 'smooth' });
        
        
        //Collapse sidebar after clicking
		if (sidebar.classList.contains('sidebar-visible') && window.innerWidth < 1200){
			
			sidebar.classList.remove('sidebar-visible');
		    sidebar.classList.add('sidebar-hidden');
		} 
		
    });
	
});


/* ===== Gumshoe SrollSpy ===== */
/* Ref: https://github.com/cferdinandi/gumshoe  */
// Initialize Gumshoe
var spy = new Gumshoe('#docs-nav a', {
	offset: 69 //sticky header height
});


/* ====== SimpleLightbox Plugin ======= */
/*  Ref: https://github.com/andreknieriem/simplelightbox */

var lightbox = new SimpleLightbox('.simplelightbox-gallery a', {/* options */});
// var found = -1;

// function search() {
 
// 	var name = document.getElementById("searchForm").elements["searchItem"].value;
// 	var pattern = name.toLowerCase();
// 	var targetId = "";
// 	// var divs = document.getElementsByClassName("docs-article");
// 	// for (var i = 0; i < divs.length; i++) {
// 	//    var para = divs[i].getElementsByTagName("h1");
// 	//    console.log(para);
// 	//    var index = para[0].innerText.toLowerCase().indexOf(pattern);	   
// 	//    console.log(index);
// 	//    if (index == -1){
// 	// 	   try {
// 	// 			para = divs[i].getElementsByTagName("p");
// 	// 			index = para[0].innerText.toLowerCase().indexOf(pattern);	  
// 	// 	   } catch (error) {
			   
// 	// 	   }
// 	//    }
// 	//    if (index != -1 && found !=i) {
// 	// 		targetId = divs[i].id;
// 	// 		found = i;
// 	// 		console.log(targetId);
// 	// 		document.getElementById(targetId).scrollIntoView();
// 	// 		break;
// 	//    }
// 	// }  
// 	// var divs = document.getElementsByClassName("docs-section");
// 	// for (var i = 0; i < divs.length; i++) {
// 	//    var para = divs[i].getElementsByTagName("h2");
// 	//    console.log(para);
// 	//    var index = para[0].innerText.toLowerCase().indexOf(pattern);	   
// 	//    console.log(index);
// 	//    if (index == -1){
// 	// 	   try {
// 	// 			para = divs[i].getElementsByTagName("p");
// 	// 			index = para[0].innerText.toLowerCase().indexOf(pattern);	  
// 	// 	   } catch (error) {
			   
// 	// 	   }
// 	//    }
// 	//    if (index != -1 && found !=i) {
// 	// 		targetId = divs[i].id;
// 	// 		found = i;
// 	// 		console.log(targetId);
// 	// 		document.getElementById(targetId).scrollIntoView();
// 	// 		break;
// 	//    }
// 	// }  
// 	var divs = document.querySelectorAll( 'body *' );
// 	for (var i = 0; i < divs.length; i++) {
// 		var para = divs[i].getElementsByTagName("p");
// 		console.log(para);
// 		try {
// 				var index = para[0].innerText.toLowerCase().indexOf(pattern);	   
// 				console.log(index);
// 		} catch (error) {
			   
// 		}

// 	   if (index != -1 && found !=i && divs[i].id!= null && divs[i].id!= "") {
// 			targetId = divs[i].id;
// 			found = i;
// 			console.log(targetId);
// 			document.getElementById(targetId).scrollIntoView();
// 			break;
// 	   }
// 	}   
// }

