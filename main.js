const problemLists = Array.from(document.querySelectorAll('a.bluebtn')).map(link => link.href)

Promise.all(problemLists.map(async url => await fetch(url))) 
        .then(data => {
        const url = URL.createObjectURL(new Blob([JSON.stringify(data.flat(), null, 2)], {type: 'application/json'}));
        const a = Object.assign(document.createElement('a'), { href: url, download: 'fetchedData.json' });
        document.body.appendChild(a);
        a.click()
        setTimeout(() => { URL.revokeObjectURL(url); document.body.removeChild(a); }, 0)
    })
