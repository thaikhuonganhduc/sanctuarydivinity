// Plugin chạy cục bộ trong Figma Desktop: nối link prototype cho file "SANCTUARY Web Prototype".
// Dùng plugin vì gói Figma Starter giới hạn số lượt gọi MCP; plugin tự chạy thì không bị giới hạn.
// Cách chạy: Figma Desktop > Plugins > Development > Import plugin from manifest... > chọn manifest.json
//            rồi mở file prototype và chạy plugin "SANCTUARY - Noi link prototype".
// Chạy lại nhiều lần vẫn an toàn: popup đã có thì không tạo lại, link chỉ bị ghi đè đúng đích.

(async () => {
  const page = figma.currentPage;
  const log = { linked: 0, skipped: 0, created: [], renamed: [] };

  // ---------- Hàm tiện ích ----------
  const frames = () => page.children.filter((n) => n.type === "FRAME");
  const byPrefix = (p) => frames().find((f) => f.name.startsWith(p));
  const clean = (s) => s.replace(/\s+/g, " ").trim();
  // Chữ hiển thị của một nút: TEXT thì lấy luôn, còn frame thì gộp chữ của các TEXT con
  const labelOf = (n) => clean(n.type === "TEXT" ? n.characters
    : ("findAll" in n ? n.findAll((c) => c.type === "TEXT").map((c) => c.characters).join(" ") : ""));
  const insideLink = (n, root) => {
    for (let p = n.parent; p && p !== root; p = p.parent) if (/^(Link|Button)/.test(p.name)) return true;
    return false;
  };
  const topFrameOf = (n) => { let p = n; while (p.parent && p.parent.type !== "PAGE") p = p.parent; return p; };

  const navigate = (dest) => ({ type: "NODE", destinationId: dest.id, navigation: "NAVIGATE",
    transition: { type: "DISSOLVE", easing: { type: "EASE_OUT" }, duration: 0.25 }, preserveScrollPosition: false });
  const overlay = (dest) => ({ type: "NODE", destinationId: dest.id, navigation: "OVERLAY",
    transition: { type: "DISSOLVE", easing: { type: "EASE_OUT" }, duration: 0.2 }, preserveScrollPosition: false });

  async function link(node, action) {
    if (!node || !action) return;
    if (action.destinationId === topFrameOf(node).id) { log.skipped++; return; } // không tự trỏ về chính trang mình
    try {
      await node.setReactionsAsync([{ trigger: { type: "ON_CLICK" }, actions: [action] }]);
      log.linked++;
    } catch (e) { log.skipped++; }
  }
  // Nối mọi nút trong frame theo bảng luật: [hàm kiểm tra node, frame đích, kiểu]
  async function wire(frame, rules) {
    if (!frame) return;
    const nodes = frame.findAll((n) => /^(Link|Button)/.test(n.name));
    for (const n of nodes) {
      const label = labelOf(n);
      for (const [test, dest, kind] of rules) {
        if (dest && test(n, label)) { await link(n, (kind === "overlay" ? overlay : navigate)(dest)); break; }
      }
    }
  }

  // ---------- Các frame đã có ----------
  const D = {
    gate: byPrefix("D01"), shop: byPrefix("D02"), cart: byPrefix("D04"), account: byPrefix("D05"),
    about: byPrefix("D06"), contact: byPrefix("D07 "), admin: byPrefix("D08 "),
  };
  const M = { gate: byPrefix("M01"), shop: byPrefix("M02"), cart: byPrefix("M04"),
    info: byPrefix("M05"), about: byPrefix("M06"), account: byPrefix("M07") };

  // ---------- 1. Nhận diện frame mới chụp: 5 tab chính sách + 7 mục Admin (desktop), Info/About/Account (mobile) ----------
  const POLICY = { "Shipping/Returns": "shipping", "Terms and Conditions": "terms", "Terms of Service": "tos",
    "Privacy Policy": "privacy", "Accessibility": "accessibility" };
  const ADMIN = { "Orders": "orders", "Products": "products", "Customers": "customers", "Messages": "messages",
    "Athlete codes": "codes", "Launch date": "launch", "Backup": "backup" };
  const MOBILE = { "Info": "info", "About": "about", "Account": "account" };   // tiêu đề h1 của trang
  const P = {}, A = {};
  const known = /^(D\d|M\d|T\d|Label|Toast)/;
  // Tiêu đề của trang/tab đang mở = chữ nằm trong bảng, không thuộc link/nút, cỡ chữ lớn nhất
  function titleOf(f, table) {
    let best = null;
    for (const t of f.findAll((n) => n.type === "TEXT")) {
      const s = clean(t.characters);
      if (!(s in table) || insideLink(t, f)) continue;
      const size = typeof t.fontSize === "number" ? t.fontSize : 0;
      if (!best || size > best.size) best = { s, size };
    }
    return best && best.s;
  }
  for (const f of frames()) {
    if (known.test(f.name) && !/^D0[78]\./.test(f.name)) continue;
    if (f.width < 600) {                                  // khung mobile (390px)
      const s = titleOf(f, MOBILE);
      if (s && !M[MOBILE[s]]) M[MOBILE[s]] = f;
      continue;
    }
    const s = titleOf(f, { ...POLICY, ...ADMIN });
    if (!s) continue;
    if (s in POLICY) P[POLICY[s]] = f; else A[ADMIN[s]] = f;
  }
  // Mobile: đặt tên M05-M07 và xếp tiếp hàng ngang sau M04 (cách nhau 510px như các khung mobile cũ)
  if (M.cart) {
    [["info", "M05 · Info"], ["about", "M06 · About"], ["account", "M07 · Account"]].forEach(([key, name], i) => {
      const f = M[key];
      if (!f) return;
      if (f.name !== name) { f.name = name; log.renamed.push(name); }
      f.x = M.cart.x + (i + 1) * 510; f.y = M.cart.y;
    });
  }
  // Đặt tên + xếp các frame mới thành cột ngay dưới trang gốc
  function arrange(base, map, order, prefix, titles) {
    if (!base) return;
    let y = base.y + base.height + 300;
    order.forEach((key, i) => {
      const f = map[key];
      if (!f) return;
      const name = `${prefix}.${i + 1} · ${titles[key]}`;
      if (f.name !== name) { f.name = name; log.renamed.push(name); }
      f.x = base.x; f.y = y; y += f.height + 300;
    });
  }
  const invert = (o) => Object.fromEntries(Object.entries(o).map(([k, v]) => [v, k]));
  arrange(D.contact, P, ["shipping", "terms", "tos", "privacy", "accessibility"], "D07", invert(POLICY));
  arrange(D.admin, A, ["orders", "products", "customers", "messages", "codes", "launch", "backup"], "D08", invert(ADMIN));

  // ---------- 2. Popup "thành công" tự tắt sau 2.5 giây ----------
  await figma.loadFontAsync({ family: "Tinos", style: "Regular" });
  await figma.loadFontAsync({ family: "Tinos", style: "Bold" });
  const C = { surface: { r: 0.078, g: 0.078, b: 0.078 }, border: { r: 0.165, g: 0.165, b: 0.165 },
    text: { r: 0.949, g: 0.949, b: 0.949 }, muted: { r: 0.541, g: 0.541, b: 0.541 } };
  // Cột popup luôn nằm bên phải mọi frame khác (không tính chính các popup)
  const isToast = (n) => n.name === "Toast / Success" || /^T0\d/.test(n.name) || n.name === "Label · POPUP";
  const rightEdge = Math.max(...page.children.filter((n) => !isToast(n)).map((n) => n.x + n.width));

  let comp = page.findOne((n) => n.type === "COMPONENT" && n.name === "Toast / Success");
  let pTitle, pBody;
  if (!comp) {
    comp = figma.createComponent();
    comp.name = "Toast / Success";
    comp.layoutMode = "HORIZONTAL";
    comp.resize(400, 100);                 // resize trước, vì resize() đưa kích thước về FIXED
    comp.primaryAxisSizingMode = "FIXED";  // rộng cố định 400
    comp.counterAxisSizingMode = "AUTO";   // cao tự co theo nội dung
    comp.itemSpacing = 16;
    comp.paddingTop = comp.paddingBottom = 20;
    comp.paddingLeft = comp.paddingRight = 24;
    comp.fills = [{ type: "SOLID", color: C.surface }];
    comp.strokes = [{ type: "SOLID", color: C.border }];
    comp.cornerRadius = 4;
    comp.effects = [{ type: "DROP_SHADOW", color: { r: 0, g: 0, b: 0, a: 0.6 }, offset: { x: 0, y: 12 },
      radius: 32, spread: 0, visible: true, blendMode: "NORMAL" }];
    const icon = figma.createNodeFromSvg('<svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="14" cy="14" r="13" stroke="#F2F2F2" stroke-width="1.5"/><path d="M8.5 14.5l3.5 3.5 7.5-8" stroke="#F2F2F2" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>');
    icon.name = "icon/check";
    comp.appendChild(icon);
    const col = figma.createFrame();
    col.name = "Content";
    col.layoutMode = "VERTICAL";
    col.itemSpacing = 6;
    col.fills = [];
    comp.appendChild(col);
    col.layoutSizingHorizontal = "FILL";
    col.layoutSizingVertical = "HUG";
    const title = figma.createText();
    title.fontName = { family: "Tinos", style: "Bold" };
    title.fontSize = 20;
    title.characters = "Title";
    title.fills = [{ type: "SOLID", color: C.text }];
    col.appendChild(title);
    const body = figma.createText();
    body.fontName = { family: "Tinos", style: "Regular" };
    body.fontSize = 15;
    body.lineHeight = { unit: "PERCENT", value: 140 };
    body.characters = "Body";
    body.fills = [{ type: "SOLID", color: C.muted }];
    col.appendChild(body);
    body.textAutoResize = "HEIGHT";
    body.layoutSizingHorizontal = "FILL";
    pTitle = comp.addComponentProperty("Title", "TEXT", "Title");
    pBody = comp.addComponentProperty("Body", "TEXT", "Body");
    title.componentPropertyReferences = { characters: pTitle };
    body.componentPropertyReferences = { characters: pBody };
    log.created.push(comp.name);
  } else {
    const defs = comp.componentPropertyDefinitions;
    pTitle = Object.keys(defs).find((k) => k.startsWith("Title"));
    pBody = Object.keys(defs).find((k) => k.startsWith("Body"));
  }
  comp.x = rightEdge + 200;   // mỗi lần chạy đều dời cột popup ra sau frame cuối cùng để không đè lên frame mới
  comp.y = 200;

  const TOASTS = [
    ["T01 · Toast · Order placed", "Order placed", "Thank you. Your order number is SD-MHX2K9. A confirmation would be sent to your email."],
    ["T02 · Toast · Signed in", "Signed in", "Welcome back. You are now signed in to your SANCTUARY account."],
    ["T03 · Toast · Account created", "Account created", "Your account is ready. Orders you place will show up in Account."],
    ["T04 · Toast · Message sent", "Message sent", "Message sent. We will reply within 48 hours."],
  ];
  const T = [];
  let ty = comp.y + comp.height + 120;
  for (const [name, title, body] of TOASTS) {
    let fr = byPrefix(name.slice(0, 3));
    if (!fr) {
      fr = figma.createFrame();
      fr.name = name;
      fr.fills = [];
      const inst = comp.createInstance();
      inst.setProperties({ [pTitle]: title, [pBody]: body });
      fr.appendChild(inst);
      fr.resize(inst.width, inst.height);
      log.created.push(name);
    }
    fr.x = comp.x;
    fr.y = ty;
    ty = fr.y + fr.height + 60;
    // Hiện 2.5 giây rồi tự đóng popup
    await fr.setReactionsAsync([{ trigger: { type: "AFTER_TIMEOUT", timeout: 2.5 }, actions: [{ type: "CLOSE" }] }]);
    T.push(fr);
  }
  const [tOrder, tSignin, tCreated, tSent] = T;

  // ---------- 3. Bảng luật nối link ----------
  const is = (name, text) => (n, l) => n.name === name && l === text;
  const starts = (name, text) => (n, l) => n.name === name && l.startsWith(text);
  const nameStarts = (prefix) => (n) => n.name.startsWith(prefix);

  // Header chung cho các trang desktop
  const header = [
    [is("Link", "Info"), D.contact], [is("Link", "About"), D.about],
    [nameStarts("Link - SANCTUARY home"), D.shop], [nameStarts("Link - Sign in"), D.account],
    [nameStarts("Link - Cart"), D.cart], [is("Button", "Exit"), D.gate],
  ];
  // Các tab trong trang Info/Contact
  const tabs = [
    [is("Link", "Contact"), D.contact], [is("Link", "Shipping/Returns"), P.shipping],
    [is("Link", "Terms and Conditions"), P.terms], [is("Link", "Terms of Service"), P.tos],
    [is("Link", "Privacy Policy"), P.privacy], [is("Link", "Accessibility"), P.accessibility],
  ];
  const faq = [
    [starts("Link", "How long does shipping"), P.shipping], [starts("Link", "Can I return"), P.shipping],
    [starts("Link", "How do athlete codes"), P.terms], [starts("Link", "What do you do with my data"), P.privacy],
    [starts("Link", "Which size should I pick"), D.shop],
  ];
  // Menu bên trái trang Admin
  const adminMenu = [
    [is("Link", "Overview"), D.admin], [is("Link", "Orders"), A.orders], [starts("Link", "Products"), A.products],
    [is("Link", "Customers"), A.customers], [is("Link", "Messages"), A.messages],
    [is("Link", "Athlete codes"), A.codes], [is("Link", "Launch date"), A.launch], [is("Link", "Backup"), A.backup],
    [nameStarts("Link - View store"), D.shop], [is("Link", "View store"), D.shop], [is("Button", "Exit"), D.gate],
  ];

  // Info/Contact và 5 tab chính sách
  for (const f of [D.contact, ...Object.values(P)]) await wire(f, [...tabs, ...faq, ...header]);
  await wire(D.contact, [[is("Button", "Send"), tSent, "overlay"]]);
  // Admin và 7 mục
  for (const f of [D.admin, ...Object.values(A)]) await wire(f, adminMenu);

  // Popup thành công cho các nút "hành động"
  await wire(D.cart, [[is("Button", "Place order"), tOrder, "overlay"]]);
  await wire(D.account, [[is("Button", "Sign in"), tSignin, "overlay"], [is("Button", "Create account"), tCreated, "overlay"]]);
  await wire(M.cart, [[is("Button", "Place order"), tOrder, "overlay"], [is("Button", "Sign in"), tSignin, "overlay"]]);

  // Mobile: header Info / About / Sign in dẫn sang 3 khung mobile mới (cùng khổ 390px, không nhảy sang desktop)
  const mobileHeader = [
    [is("Link", "Info"), M.info], [is("Link", "About"), M.about],
    [nameStarts("Link - SANCTUARY home"), M.shop], [nameStarts("Link - Sign in"), M.account],
    [nameStarts("Link - Cart"), M.cart], [is("Button", "Exit"), M.gate],
  ];
  for (const f of [M.shop, M.cart, M.info, M.about, M.account]) await wire(f, mobileHeader);
  await wire(M.info, [[starts("Link", "Which size should I pick"), M.shop], [is("Button", "Send"), tSent, "overlay"]]);
  await wire(M.account, [[is("Button", "Sign in"), tSignin, "overlay"], [is("Button", "Create account"), tCreated, "overlay"]]);

  // Thêm điểm bắt đầu "Admin flow" để xem riêng luồng quản trị
  if (D.admin && !page.flowStartingPoints.some((p) => p.nodeId === D.admin.id)) {
    page.flowStartingPoints = [...page.flowStartingPoints, { nodeId: D.admin.id, name: "Admin flow" }];
  }

  const mobileFound = ["info", "about", "account"].filter((k) => M[k]).length;
  const msg = `Đã nối ${log.linked} link · tab chính sách: ${Object.keys(P).length}/5 · mục Admin: ${Object.keys(A).length}/7 · mobile mới: ${mobileFound}/3 · tạo mới: ${log.created.length}`;
  console.log(msg, log);
  figma.closePlugin(msg);
})().catch((e) => figma.closePlugin("Lỗi: " + e.message));
