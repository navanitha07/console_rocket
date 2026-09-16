const API = "/api";
let state = {students: [], organizers: [], events: [], registrations: []};

async function request(path, options = {}) {
    const response = await fetch(API + path, {
        headers: {"Content-Type": "application/json"},
        ...options
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || "Request failed");
    return data;
}

function toast(message, error = false) {
    const t = document.getElementById("toast");
    t.textContent = message;
    t.style.background = error ? "#c94d5b" : "#20263a";
    t.classList.add("show");
    setTimeout(() => t.classList.remove("show"), 2800);
}

function closeModal() {
    document.getElementById("modal").classList.add("hidden");
}

function showModal(html) {
    document.getElementById("modal-content").innerHTML = html;
    document.getElementById("modal").classList.remove("hidden");
}

function fmtDate(value) {
    return new Date(value).toLocaleDateString("en-IN", {
        day: "2-digit", month: "short", year: "numeric"
    });
}

function studentName(id) {
    return state.students.find(x => x.stu_id === id)?.stu_name || "Unknown";
}

function eventName(id) {
    return state.events.find(x => x.event_id === id)?.event_name || "Unknown";
}

function organizerName(id) {
    return state.organizers.find(x => x.organizer_id === id)?.name || "Unknown";
}

document.querySelectorAll(".nav-item").forEach(btn => {
    btn.onclick = () => switchPage(btn.dataset.page);
});

async function switchPage(page) {
    document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
    document.getElementById(page).classList.add("active");
    document.querySelectorAll(".nav-item").forEach(
        b => b.classList.toggle("active", b.dataset.page === page)
    );
    document.getElementById("page-title").textContent =
        page[0].toUpperCase() + page.slice(1);

    try {
        await loadAllData();
        if (page === "dashboard") loadDashboard();
        if (page === "events") renderEvents();
        if (page === "registrations") renderRegistrations();
        if (page === "students") renderStudents();
        if (page === "organizers") renderOrganizers();
    } catch (e) {
        toast(e.message, true);
    }
}

async function loadAllData() {
    [state.students, state.organizers, state.events, state.registrations] =
        await Promise.all([
            request("/students"),
            request("/organizers"),
            request("/events"),
            request("/registrations")
        ]);
}

async function loadDashboard() {
    try {
        await loadAllData();
        const summary = await request("/events/highest-registrations");
        const active = state.registrations.filter(x => x.status !== "CANCELLED").length;
        const checked = state.registrations.filter(x => x.status === "CHECKED_IN").length;

        document.getElementById("stat-events").textContent = state.events.length;
        document.getElementById("stat-students").textContent = state.students.length;
        document.getElementById("stat-registrations").textContent = active;
        document.getElementById("stat-checkins").textContent = checked;
        document.getElementById("hero-checkins").textContent = checked;

        document.getElementById("ranking").innerHTML = summary.map(e => {
            const pct = Math.min(100, Math.round(e.registered_count / e.capacity * 100));
            return `<div class="event-card">
                <span class="badge">${e.status}</span>
                <h4>${e.event_name}</h4>
                <div class="event-meta">📅 ${fmtDate(e.event_date)}<br>Capacity: ${e.capacity}</div>
                <div class="progress"><i style="width:${pct}%"></i></div>
                <div class="card-row"><span>${e.registered_count} registered</span><b>${e.checked_in_count} checked in</b></div>
            </div>`;
        }).join("") || `<div class="empty">No events yet.</div>`;
    } catch (e) {
        toast(e.message, true);
    }
}

function table(headers, rows) {
    return `<table class="data-table"><thead><tr>
        ${headers.map(h => `<th>${h}</th>`).join("")}
    </tr></thead><tbody>${rows || `<tr><td colspan="${headers.length}"><div class="empty">No data found.</div></td></tr>`}</tbody></table>`;
}

async function renderEvents() {
    const rows = state.events.map(e => `<tr>
        <td><b>${e.event_name}</b></td>
        <td>${organizerName(e.organizer_id)}</td>
        <td>${fmtDate(e.event_date)}</td>
        <td>${e.maximum_capacity}</td>
        <td><span class="badge">${e.status}</span></td>
        <td><button class="action" onclick="editEvent(${e.event_id})">Edit</button>
            <button class="action danger" onclick="deleteEntity('/events/${e.event_id}',renderEvents)">Delete</button></td>
    </tr>`).join("");
    document.getElementById("events-list").innerHTML =
        table(["EVENT","ORGANIZER","DATE","CAPACITY","STATUS","ACTIONS"], rows);
}

async function renderRegistrations() {
    const rows = state.registrations.map(r => {
        const cls = r.status === "CHECKED_IN" ? "green" : r.status === "CANCELLED" ? "red" : "";
        return `<tr><td>#${r.registration_id}</td><td><b>${studentName(r.stu_id)}</b></td>
            <td>${eventName(r.event_id)}</td><td><span class="badge ${cls}">${r.status}</span></td>
            <td>${r.check_in_time ? new Date(r.check_in_time).toLocaleTimeString([], {hour:"2-digit",minute:"2-digit"}) : "—"}</td>
            <td>${r.status === "REGISTERED" ?
                `<button class="action" onclick="checkIn(${r.registration_id})">Check in</button>
                 <button class="action danger" onclick="cancelReg(${r.registration_id})">Cancel</button>` : ""}
                <button class="action danger" onclick="deleteEntity('/registrations/${r.registration_id}',renderRegistrations)">Delete</button></td>
        </tr>`;
    }).join("");
    document.getElementById("registrations-list").innerHTML =
        table(["ID","STUDENT","EVENT","STATUS","CHECK-IN","ACTIONS"], rows);
}

async function renderStudents() {
    const rows = state.students.map(s => `<tr>
        <td>#${s.stu_id}</td><td><b>${s.stu_name}</b></td><td>${s.department || "—"}</td><td>${s.phone_no || "—"}</td>
        <td><button class="action" onclick="editStudent(${s.stu_id})">Edit</button>
            <button class="action danger" onclick="deleteEntity('/students/${s.stu_id}',renderStudents)">Delete</button></td>
    </tr>`).join("");
    document.getElementById("students-list").innerHTML =
        table(["ID","NAME","DEPARTMENT","PHONE","ACTIONS"], rows);
}

async function renderOrganizers() {
    const rows = state.organizers.map(o => `<tr>
        <td>#${o.organizer_id}</td><td><b>${o.name}</b></td>
        <td><button class="action" onclick="editOrganizer(${o.organizer_id})">Edit</button>
            <button class="action danger" onclick="deleteEntity('/organizers/${o.organizer_id}',renderOrganizers)">Delete</button></td>
    </tr>`).join("");
    document.getElementById("organizers-list").innerHTML =
        table(["ID","NAME","ACTIONS"], rows);
}

function openEventModal(event = null) {
    showModal(`<div class="eyebrow">${event ? "EDIT" : "CREATE"} EVENT</div>
        <h3>${event ? "Edit event" : "Create a new event"}</h3><br>
        <form onsubmit="saveEvent(event,${event?.event_id || "null"});return false">
        <div class="form-grid">
          <div class="form-group full"><label>EVENT NAME</label><input id="ev-name" required value="${event?.event_name || ""}"></div>
          <div class="form-group"><label>ORGANIZER</label><select id="ev-org">${state.organizers.map(o =>
            `<option value="${o.organizer_id}" ${event?.organizer_id === o.organizer_id ? "selected" : ""}>${o.name}</option>`).join("")}</select></div>
          <div class="form-group"><label>MAXIMUM CAPACITY</label><input id="ev-cap" type="number" min="1" required value="${event?.maximum_capacity || 50}"></div>
          <div class="form-group"><label>EVENT DATE</label><input id="ev-date" type="date" required value="${event ? event.event_date.slice(0,10) : ""}"></div>
          <div class="form-group"><label>STATUS</label><select id="ev-status"><option ${!event || event.status === "Open" ? "selected" : ""}>Open</option><option ${event?.status === "Closed" ? "selected" : ""}>Closed</option></select></div>
          <div class="form-group"><label>START TIME</label><input id="ev-start" type="time" value="${event?.start_time || "10:00"}"></div>
          <div class="form-group"><label>END TIME</label><input id="ev-end" type="time" value="${event?.end_time || "13:00"}"></div>
        </div>
        <div class="form-actions"><button type="button" class="ghost" onclick="closeModal()">Cancel</button><button class="primary">Save Event</button></div>
        </form>`);
}

async function saveEvent(_, id) {
    try {
        const body = {
            event_name: document.getElementById("ev-name").value,
            organizer_id: +document.getElementById("ev-org").value,
            maximum_capacity: +document.getElementById("ev-cap").value,
            status: document.getElementById("ev-status").value,
            event_date: document.getElementById("ev-date").value + "T00:00:00",
            start_time: document.getElementById("ev-start").value,
            end_time: document.getElementById("ev-end").value
        };
        await request(id ? `/events/${id}` : "/events", {
            method: id ? "PUT" : "POST",
            body: JSON.stringify(body)
        });
        closeModal(); toast("Event saved"); await loadAllData(); renderEvents();
    } catch (e) { toast(e.message, true); }
}

async function editEvent(id) {
    await loadAllData();
    openEventModal(state.events.find(e => e.event_id === id));
}

function openStudentModal(student = null) {
    showModal(`<div class="eyebrow">${student ? "EDIT" : "ADD"} STUDENT</div><h3>${student ? "Edit student" : "Add a student"}</h3><br>
    <form onsubmit="saveStudent(event,${student?.stu_id || "null"});return false"><div class="form-grid">
    <div class="form-group full"><label>STUDENT NAME</label><input id="st-name" required value="${student?.stu_name || ""}"></div>
    <div class="form-group"><label>DEPARTMENT</label><input id="st-dept" value="${student?.department || ""}"></div>
    <div class="form-group"><label>PHONE NUMBER</label><input id="st-phone" value="${student?.phone_no || ""}"></div>
    </div><div class="form-actions"><button type="button" class="ghost" onclick="closeModal()">Cancel</button><button class="primary">Save Student</button></div></form>`);
}

async function saveStudent(_, id) {
    try {
        const body = {stu_name: document.getElementById("st-name").value, department: document.getElementById("st-dept").value, phone_no: document.getElementById("st-phone").value};
        await request(id ? `/students/${id}` : "/students", {method:id ? "PUT":"POST", body:JSON.stringify(body)});
        closeModal(); toast("Student saved"); await loadAllData(); renderStudents();
    } catch(e) { toast(e.message,true); }
}

async function editStudent(id) { await loadAllData(); openStudentModal(state.students.find(s => s.stu_id === id)); }

function openOrganizerModal(org = null) {
    showModal(`<div class="eyebrow">${org ? "EDIT" : "ADD"} ORGANIZER</div><h3>${org ? "Edit organizer" : "Add an organizer"}</h3><br>
    <form onsubmit="saveOrganizer(event,${org?.organizer_id || "null"});return false">
    <div class="form-group"><label>ORGANIZER NAME</label><input id="org-name" required value="${org?.name || ""}"></div>
    <div class="form-actions"><button type="button" class="ghost" onclick="closeModal()">Cancel</button><button class="primary">Save Organizer</button></div></form>`);
}

async function saveOrganizer(_, id) {
    try {
        await request(id ? `/organizers/${id}` : "/organizers", {
            method:id ? "PUT":"POST",
            body:JSON.stringify({name:document.getElementById("org-name").value})
        });
        closeModal(); toast("Organizer saved"); await loadAllData(); renderOrganizers();
    } catch(e) { toast(e.message,true); }
}

async function editOrganizer(id) { await loadAllData(); openOrganizerModal(state.organizers.find(o => o.organizer_id === id)); }

function openRegistrationModal() {
    showModal(`<div class="eyebrow">REGISTRATION</div><h3>Register a student</h3><br>
    <form onsubmit="saveRegistration(event);return false"><div class="form-grid">
    <div class="form-group"><label>STUDENT</label><select id="reg-st">${state.students.map(s => `<option value="${s.stu_id}">${s.stu_name}</option>`).join("")}</select></div>
    <div class="form-group"><label>EVENT</label><select id="reg-ev">${state.events.map(e => `<option value="${e.event_id}">${e.event_name}</option>`).join("")}</select></div>
    </div><div class="form-actions"><button type="button" class="ghost" onclick="closeModal()">Cancel</button><button class="primary">Register</button></div></form>`);
}

async function saveRegistration() {
    try {
        await request("/registrations", {method:"POST", body:JSON.stringify({
            stu_id:+document.getElementById("reg-st").value,
            event_id:+document.getElementById("reg-ev").value,
            status:"REGISTERED"
        })});
        closeModal(); toast("Registration created"); await loadAllData(); renderRegistrations();
    } catch(e) { toast(e.message,true); }
}

async function checkIn(id) {
    try { await request(`/registrations/${id}/check-in`,{method:"POST"}); toast("Student checked in"); await loadAllData(); renderRegistrations(); }
    catch(e) { toast(e.message,true); }
}

async function cancelReg(id) {
    try { await request(`/registrations/${id}/cancel`,{method:"POST"}); toast("Registration cancelled"); await loadAllData(); renderRegistrations(); }
    catch(e) { toast(e.message,true); }
}

async function deleteEntity(path, refresh) {
    if (!confirm("Delete this record?")) return;
    try { await request(path,{method:"DELETE"}); toast("Deleted successfully"); await loadAllData(); refresh(); }
    catch(e) { toast(e.message,true); }
}

loadDashboard();
