$(document).ready(function () {
  $("#reviewsTable").DataTable({
    paging: false,
    scrollCollapse: true,
    scrollY: "60vh",
    lengthChange: true,
    lengthMenu: [
      [5, 10, 25, -1],
      [5, 10, 25, "All"]
    ],
    ordering: true,
    columns: [
      { width: "10%" }, // Review ID
      { width: "10%" }, // Author
      { width: "5%" }, // Recommendation
      { width: "5%" }, // Stars
      { width: "10%" }, // Review Date
      { width: "55%" } // Content
    ]
  });
});
