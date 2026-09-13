function updatePlatform(checkbox, postId, platform) {
    const isChecked = checkbox.checked;

    fetch('/update_platform', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id: postId,
            platform: platform,
            value: isChecked
        })
    }).then(response => {
        if (!response.ok) {
            alert('Failed to update platform status.');
            checkbox.checked = !isChecked; // Revert visually if failed
        }
    });
}

function deletePost(postId) {
    if (confirm("Are you sure you want to delete this idea?")) {
        fetch(`/delete/${postId}`, {
            method: 'POST'
        }).then(response => {
            if (response.ok) {
                const card = document.getElementById(`card-${postId}`);
                if (card) {
                    card.remove(); // Removes the card without reloading the page
                }
            } else {
                alert('Failed to delete post.');
            }
        });
    }
}

let draggedCardId = null;

function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev, postId) {
    draggedCardId = postId;
}

function drop(ev, newStatus) {
    ev.preventDefault();
    if (!draggedCardId) return;

    fetch('/update_status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id: draggedCardId,
            status: newStatus
        })
    }).then(response => {
        if (response.ok) {
            window.location.reload(); // Quick refresh to re-render columns
        } else {
            alert('Failed to move card.');
        }
    });
}
