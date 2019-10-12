$("input").keyup(function() {
    let query = $(this).val()

    $.ajax({
        type: "POST",
        url: "/query",
        data: {
            query: query
        },
        success: function(songs){
            $("#results").empty()
            songs.forEach(function(song) {
                let elem = createElem(song)
                $("#results").append(elem)
            });
        }
    });
});

function createElem(song) {
    let link = document.createElement("a")
    link.href = song["song_link"]

    let name = document.createElement("span")
    name.className = "song"
    name.innerText = song["song_name"]
    link.append(name)

    let artist = document.createElement("span")
    artist.className = "artist"
    artist.innerHTML = " by " + song["artist_name"]
    link.append(artist)

    return link
}