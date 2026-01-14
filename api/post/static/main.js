let page = 2;
let hasNext = true;
let loading = false;

window.addEventListener("scroll", () => {
    if (loading || !hasNext) return;

    const scrollBottom =
        window.innerHeight + window.scrollY >= document.body.offsetHeight - 100;
    console.log("scroll")
    if (scrollBottom) {
        loadMore();
    }
});


function loadMore() {
    loading = true;
    document.getElementById("loading").style.display = "block";

    fetch(`/feed/api/?page=${page}`)
        .then(res => res.json())
        .then(data => {
            console.log(data);
            data.posts.forEach(post => {
                const div = document.createElement("div");
                div.className = "post";
                div.innerHTML = `
                        <h3>${post.titulo}</h3>
                        <p>${post.conteudo}</p>
                        <small>${post.criado_em}</small>
                    `;
                document.getElementById("feed").appendChild(div);
            });

            hasNext = data.has_next;
            page++;
            loading = false;
            document.getElementById("loading").style.display = "none";
        });
}
loadMore()