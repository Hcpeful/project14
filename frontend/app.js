const API = "http://localhost:3001/calculations";

async function load() {
  const res = await fetch(API);
  const data = await res.json();

  const list = document.getElementById("list");
  list.innerHTML = "";

  data.forEach(c => {
    const li = document.createElement("li");
    li.innerText = `${c.operation}: ${c.operandA}, ${c.operandB} = ${c.result}`;

    const del = document.createElement("button");
    del.innerText = "Delete";
    del.onclick = async () => {
      await fetch(`${API}/${c.id}`, { method: "DELETE" });
      load();
    };

    li.appendChild(del);
    list.appendChild(li);
  });
}

document.getElementById("calc-form").onsubmit = async e => {
  e.preventDefault();

  await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      operation: operation.value,
      operandA: a.value,
      operandB: b.value
    })
  });

  load();
};

load();
