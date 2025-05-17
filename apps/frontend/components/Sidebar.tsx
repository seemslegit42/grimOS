export function Sidebar() {
  return (
    <aside className="w-64 bg-gray-800 text-white h-screen p-4">
      <nav>
        <ul>
          <li className="mb-2"><a href="#" className="hover:underline">Dashboard</a></li>
          <li className="mb-2"><a href="#" className="hover:underline">Settings</a></li>
          <li><a href="#" className="hover:underline">Profile</a></li>
        </ul>
      </nav>
    </aside>
  );
}
